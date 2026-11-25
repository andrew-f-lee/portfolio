from pathlib import Path
import argparse
import json
import re
import sqlite3
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import chi2_contingency, norm
from download_data import TABLES

def analysis(data):
    frames = {table: pd.read_csv(data / f"olist_{table}_dataset.csv") for table in TABLES}
    with sqlite3.connect(":memory:") as db:
        for table, frame in frames.items():
            frame.to_sql(table, db, index=False)
        db.execute("CREATE INDEX customer_lookup ON customers(customer_id)")
        db.execute("CREATE INDEX order_lookup ON orders(order_id)")
        sql = Path(__file__).with_name("queries.sql").read_text()
        segments = re.split(r"(?m)^-- [1-8]\. ", sql)
        db.executescript(segments[0])
        outputs = [pd.read_sql_query("-- " + segment, db) for segment in segments[1:]]
    o = frames["orders"].merge(frames["customers"][["customer_id","customer_unique_id","customer_state"]], on="customer_id", validate="one_to_one")
    o["purchase"] = pd.to_datetime(o.order_purchase_timestamp)
    o["delivered"] = pd.to_datetime(o.order_delivered_customer_date)
    o["estimate"] = pd.to_datetime(o.order_estimated_delivery_date)
    o = o.sort_values(["purchase","order_id"])
    delivered_cutoff = o.loc[o.order_status.eq("delivered"),"purchase"].max()
    e = o.loc[~o.order_status.isin(["canceled","unavailable"])].copy()
    eligible_repeat = e.groupby("customer_unique_id").order_id.nunique()
    assert len(eligible_repeat) == outputs[1].customers.iloc[0]
    assert eligible_repeat.ge(2).sum() == outputs[1].repeat_customers.iloc[0]
    first = e.drop_duplicates("customer_unique_id").set_index("customer_unique_id")
    second = e.loc[e.groupby("customer_unique_id").cumcount().eq(1)].set_index("customer_unique_id").purchase
    first["repeated"] = second.le(first.purchase + pd.Timedelta(days=90)).reindex(first.index,fill_value=False)
    first = first.loc[first.order_status.eq("delivered") & first.delivered.notna() & first.estimate.notna()
                      & first.purchase.le(delivered_cutoff - pd.Timedelta(days=90))].copy()
    first["late"] = first.delivered.dt.normalize().gt(first.estimate.dt.normalize())
    counts = first.groupby("late").repeated.agg(["size","sum"]).astype(int)
    assert np.array_equal(counts.values,outputs[7][["first_orders","repeats"]].values)
    n0,n1 = counts["size"].tolist()
    v0,v1 = counts["sum"].tolist()
    a,b = v0/n0,v1/n1
    chi,p,_,_ = chi2_contingency([[v0,n0-v0],[v1,n1-v1]],correction=False)
    se = np.sqrt(a*(1-a)/n0+b*(1-b)/n1)
    # Adjust for calendar month of first order and customer state.
    first["cohort"] = first.purchase.dt.to_period("M").astype(str)
    groups = first.groupby(["late","cohort","customer_state"]).repeated.agg(["size","sum"]).reset_index()
    x = pd.get_dummies(groups[["cohort","customer_state"]],drop_first=True,dtype=float).to_numpy()
    x = np.column_stack([np.ones(len(groups)),groups.late.astype(float),x])
    n,y = groups["size"].to_numpy(),groups["sum"].to_numpy()
    def loss(beta):
       z=x@beta
       return (np.logaddexp(0,z)*n-y*z).sum(),x.T@(n*expit(z)-y)
    b0=np.zeros(x.shape[1]);b0[0]=-4
    fit = minimize(loss,b0,jac=True,method="BFGS",options={"gtol":1e-6,"maxiter":1000})
    grad = np.linalg.norm(loss(fit.x)[1],ord=np.inf)
    if grad>1e-3: raise ValueError(f"Logistic optimizer gradient {grad}")
    pred=expit(x@fit.x)
    cov=np.linalg.pinv((x.T*(n*pred*(1-pred)))@x)
    coef=fit.x[1]; sd=np.sqrt(cov[1,1])
    review=frames["order_reviews"].groupby("order_id").review_score.mean()
    dr=o.loc[o.order_status.eq("delivered") & o.delivered.notna() & o.estimate.notna()].copy()
    dr["late"]=dr.delivered.dt.normalize().gt(dr.estimate.dt.normalize())
    dr["stars"]=dr.order_id.map(review)
    summary = {
      "orders":len(o),"unique":int(o.customer_unique_id.nunique()),
      "raw_order_customer_ids":int(o.customer_id.nunique()),"duplicate_order_ids":int(o.order_id.duplicated().sum()),
      "start":str(o.purchase.min().date()),"end":str(o.purchase.max().date()),"cutoff":str(delivered_cutoff.date()),
      "eligible":int(len(e)),"eligible_customers":int(len(eligible_repeat)),"repeat_customers":int(eligible_repeat.ge(2).sum()),
      "on_time_n":n0,"late_n":n1,"on_time_repeats":v0,"late_repeats":v1,"on_time":a,"late":b,"difference":b-a,
      "diff_ci":[b-a-1.96*se,b-a+1.96*se],"chi_square":chi,"chi_p":p,
      "odds_ratio":np.exp(coef),"odds_ci":[np.exp(coef-1.96*sd),np.exp(coef+1.96*sd)],"logit_p":2*norm.sf(abs(coef/sd)),
      "logit_gradient":grad,
      "late_stars":dr.groupby("late").stars.mean().loc[True],"on_time_stars":dr.groupby("late").stars.mean().loc[False],
      "audit":{key:{"rows":len(frame),"duplicate_rows":int(frame.duplicated().sum()),"nulls":{c:int(v) for c,v in frame.isna().sum().items() if v}} for key,frame in frames.items()},
    }
    return summary,outputs

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("data",type=Path,nargs="?",default=Path("data"))
    parser.add_argument("--output",type=Path,default=Path("analysis-output"))
    args=parser.parse_args()
    args.output.mkdir(exist_ok=True,parents=True)
    summary,tables=analysis(args.data)
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2))
    for i,table in enumerate(tables,1): table.to_csv(args.output/f"query-{i}.csv",index=False)
    print(json.dumps({k:v for k,v in summary.items() if k!="audit"},indent=2))

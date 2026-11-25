-- Shared preparation. Eligible orders contain one row per order.
CREATE TEMP VIEW eligible AS
SELECT o.*,c.customer_unique_id
FROM orders o JOIN customers c USING(customer_id)
WHERE o.order_status NOT IN ('canceled','unavailable');
CREATE TEMP VIEW ranked AS
SELECT *, row_number() OVER (PARTITION BY customer_unique_id ORDER BY order_purchase_timestamp,order_id) AS rn
FROM eligible;
CREATE TEMP VIEW first_orders AS SELECT * FROM ranked WHERE rn=1;
CREATE TEMP VIEW paid AS SELECT order_id,sum(payment_value) AS payment FROM order_payments GROUP BY 1;
CREATE TEMP VIEW review AS SELECT order_id,avg(review_score) AS stars FROM order_reviews GROUP BY 1;
CREATE TEMP VIEW repeaters AS
SELECT customer_unique_id,count(DISTINCT order_id) AS n FROM eligible GROUP BY 1;

-- 1. Monthly qualifying orders and observed payments (BRL).
SELECT substr(order_purchase_timestamp,1,7) AS month,count(*) AS orders,
       sum(coalesce(payment,0)) AS observed_payments
FROM eligible LEFT JOIN paid USING(order_id) GROUP BY 1 ORDER BY 1;

-- 2. Qualifying customers and observed repeat share.
SELECT count(*) AS customers,sum(n>=2) AS repeat_customers,avg(n>=2) AS repeat_rate
FROM repeaters;

-- 3. First-order cohorts and observed repeat share (unequal observation windows).
SELECT substr(f.order_purchase_timestamp,1,7) AS cohort,count(*) AS customers,
       sum(n>=2) AS repeat_customers,avg(n>=2) AS repeat_rate
FROM first_orders f JOIN repeaters USING(customer_unique_id) GROUP BY 1 ORDER BY 1;

-- 4. Exact calendar-month retention. Suppress immature observation cells.
WITH month_offsets(k) AS (VALUES(1),(3),(6)), counts AS (
 SELECT substr(f.order_purchase_timestamp,1,7) AS cohort,k,
        count(DISTINCT f.customer_unique_id) AS cohort_size,
        count(DISTINCT CASE WHEN r.order_id IS NOT NULL THEN f.customer_unique_id END) AS retained
 FROM first_orders f CROSS JOIN month_offsets
 LEFT JOIN ranked r ON r.customer_unique_id=f.customer_unique_id AND r.rn>1
 AND date(r.order_purchase_timestamp,'start of month')=date(f.order_purchase_timestamp,'start of month','+'||k||' months')
 WHERE date(f.order_purchase_timestamp,'start of month','+'||(k+1)||' months','-1 day')
 <= (SELECT date(max(order_purchase_timestamp)) FROM orders WHERE order_status='delivered')
 GROUP BY 1,2
) SELECT *,1.0*retained/cohort_size AS retention FROM counts ORDER BY 1,2;

-- 5. Average delivery and promised time for delivered orders with valid timestamps.
SELECT substr(order_purchase_timestamp,1,7) AS month,
 avg(julianday(order_delivered_customer_date)-julianday(order_purchase_timestamp)) AS delivery_days,
 avg(julianday(order_estimated_delivery_date)-julianday(order_purchase_timestamp)) AS estimated_days
FROM eligible WHERE order_status='delivered' AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL GROUP BY 1 ORDER BY 1;

-- 6. Delivery-days distribution and mean order-level review score.
SELECT CASE WHEN days<=3 THEN '0–3' WHEN days<=7 THEN '4–7' WHEN days<=14 THEN '8–14'
 WHEN days<=30 THEN '15–30' ELSE '31+' END AS days_band,
 count(*) AS reviewed_orders,avg(stars) AS stars,
 avg(CASE WHEN late THEN stars END) AS late_stars, avg(CASE WHEN NOT late THEN stars END) AS on_time_stars
FROM (SELECT CAST(julianday(e.order_delivered_customer_date)-julianday(e.order_purchase_timestamp) AS INTEGER) AS days,
 date(e.order_delivered_customer_date)>date(e.order_estimated_delivery_date) AS late,stars
 FROM eligible e JOIN review USING(order_id) WHERE e.order_status='delivered'
 AND e.order_delivered_customer_date IS NOT NULL AND e.order_estimated_delivery_date IS NOT NULL)
WHERE days>=0 GROUP BY 1 ORDER BY min(days);

-- 7. Item value, and customer-level observed repeat rate within each category.
WITH category_items AS (
 SELECT coalesce(p.product_category_name,'unknown') AS category,e.customer_unique_id,i.price
 FROM order_items i JOIN eligible e USING(order_id) LEFT JOIN products p USING(product_id)
), category_customers AS (
 SELECT category,customer_unique_id,sum(price) AS value FROM category_items GROUP BY 1,2
) SELECT category,sum(value) AS item_value,count(*) AS customers,avg(n>=2) AS repeat_rate
FROM category_customers JOIN repeaters USING(customer_unique_id) GROUP BY 1 ORDER BY 2 DESC;

-- 8. Ninety-day repeat after first purchase, with equal follow-up.
-- Restrict to delivered first orders and first purchases at least 90 days before last delivery-order purchase.
SELECT date(f.order_delivered_customer_date)>date(f.order_estimated_delivery_date) AS late,
 count(*) AS first_orders,
 sum(CASE WHEN julianday(r.order_purchase_timestamp)<=julianday(f.order_purchase_timestamp)+90 THEN 1 ELSE 0 END) AS repeats
FROM first_orders f
LEFT JOIN (SELECT customer_unique_id,order_purchase_timestamp FROM ranked WHERE rn=2) r
ON r.customer_unique_id=f.customer_unique_id
WHERE f.order_status='delivered' AND f.order_estimated_delivery_date IS NOT NULL
 AND f.order_delivered_customer_date IS NOT NULL
 AND julianday(f.order_purchase_timestamp)+90<=(SELECT julianday(max(order_purchase_timestamp)) FROM orders WHERE order_status='delivered')
GROUP BY 1 ORDER BY 1;

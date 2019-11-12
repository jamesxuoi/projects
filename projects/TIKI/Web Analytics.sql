#standardSQL
with data1 as(
SELECT count(*)
FROM `kpmg-249807.KPMG.KPMG_demo`
where product_line is null
),

data2 as(
SELECT count(*)
FROM `kpmg-249807.KPMG.KPMG_demo`
where online_order is null
),

data_union as (
select * from data1
union all
select * from data2
),

select_order_and_status_notnull as(
select *
FROM `kpmg-249807.KPMG.KPMG_demo`
where order_status is not null
and online_order is not null
),

fill_null as(
select *, 
  ifnull(online_order, 100000) as online_order_fill
from `kpmg-249807.KPMG.KPMG_demo`
),

describe_data as(
select 
  min(list_price) as min ,
  max(list_price) as max,
  avg(list_price) as avg,
  count(distinct list_price) as num_price_unique,
  count(list_price) as num_price
from `kpmg-249807.KPMG.KPMG_demo` 
),

list_price_data as(
select
  list_price,
  count(*) as num_price
from `kpmg-249807.KPMG.KPMG_demo` 
group by list_price
order by num_price DESC
-- order by 2 DESC
--by name hoac by number ordinal column
),

gap_data as(
select
  *,
  list_price - standard_cost as gap
from `kpmg-249807.KPMG.KPMG_demo` 
),

direct_avg_gap as(
select avg(list_price - standard_cost) as avg_gap
from `kpmg-249807.KPMG.KPMG_demo` 
)

select * from gap_data 
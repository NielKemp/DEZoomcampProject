
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}
select t1.*, t2.country
from {{source('yield_staging', 'wheat')}} t1
left join {{source('yield_staging', 'geo_coords')}} t2 on t1.lat = t1.lat and t1.long = t2.long

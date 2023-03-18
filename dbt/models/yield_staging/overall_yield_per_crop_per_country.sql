
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/
{{ config(materialized='table') }}

select  t1.lat, 
        t1.long, 
        t1.year,
        t2.country,
        t1.yield as maize_yield, 
        t3.yield as maize_major_yield,
        t4.yield as maize_second_yield,
        t5.yield as rice_yield,
        t6.yield as rice_major_yield,
        t7.yield as rice_minor_yield,
        t8.yield as soybean_yield,
        t9.yield as wheat_yield,
        t10.yield as wheat_spring_yield,   
        t11.yield as wheat_winter_yield,

from        {{source('staging','maize')}}            t1
left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long
left join   {{source('staging','maize_major')}}     t3 on t1.lat = t3.lat and t1.long = t3.long     and t1.year = t3.year
left join   {{source('staging','maize_second')}}    t4 on t1.lat = t4.lat and t1.long = t4.long     and t1.year = t4.year
left join   {{source('staging','rice')}}            t5 on t1.lat = t5.lat and t1.long = t5.long     and t1.year = t5.year
left join   {{source('staging','rice_major')}}      t6 on t1.lat = t6.lat and t1.long = t6.long     and t1.year = t6.year
left join   {{source('staging','rice_second')}}     t7 on t1.lat = t7.lat and t1.long = t7.long     and t1.year = t7.year
left join   {{source('staging','soybean')}}         t8 on t1.lat = t8.lat and t1.long = t8.long     and t1.year = t8.year
left join   {{source('staging','wheat')}}           t9 on t1.lat = t9.lat and t1.long = t9.long     and t1.year = t9.year
left join   {{source('staging','wheat_spring')}}    t10 on t1.lat = t10.lat and t1.long = t10.long  and t1.year = t10.year
left join   {{source('staging','wheat_winter')}}    t11 on t1.lat = t11.lat and t1.long = t11.long  and t1.year = t11.year





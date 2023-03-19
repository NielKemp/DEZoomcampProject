{{ config(
    materialized='table',
     partition_by={
      "field": "year",
      "data_type": "int64",
      "range": {
        "start": 1982,
        "end": 2015,
        "interval": 1
    }},
    cluster_by = ["country"]
)}}

select  t1.lat, 
        t1.long, 
        t1.year,
        t2.country,
        coalesce(t1.yield,0) as maize_yield, 
        coalesce(t3.yield,0) as maize_major_yield,
        coalesce(t4.yield,0) as maize_second_yield,
        coalesce(t5.yield,0) as rice_yield,
        coalesce(t6.yield,0) as rice_major_yield,
        coalesce(t7.yield,0) as rice_minor_yield,
        coalesce(t8.yield,0) as soybean_yield,
        coalesce(t9.yield,0) as wheat_yield,
        coalesce(t10.yield,0) as wheat_spring_yield,   
        coalesce(t11.yield,0) as wheat_winter_yield,
        coalesce(t1.yield,0) +
        coalesce(t3.yield,0) +
        coalesce(t4.yield,0) +
        coalesce(t5.yield,0) +
        coalesce(t6.yield,0) +
        coalesce(t7.yield,0) +
        coalesce(t8.yield,0) +
        coalesce(t9.yield,0) +
        coalesce(t10.yield,0) +
        coalesce(t11.yield,0)  as total_yield



from        {{source('staging','maize')}}           t1
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





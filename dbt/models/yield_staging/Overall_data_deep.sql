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
    cluster_by = ["country", "crop"]
)}}


with maize as 
(
    select  t1.lat, 
            t1.long,
            'maize' as crop, 
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','maize')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

maize_major as 
(
    select  t1.lat, 
            t1.long, 
            'maize_major' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','maize_major')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

maize_second as 
(
    select  t1.lat, 
            t1.long, 
            'maize_second' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','maize_second')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

rice as 
(
    select  t1.lat, 
            t1.long, 
            'rice' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','rice')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

rice_major as 
(
    select  t1.lat, 
            t1.long,
            'rice_major' as crop, 
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','rice_major')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

rice_second as 
(
    select  t1.lat, 
            t1.long,
            'rice_second' as crop, 
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','rice_second')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

soybean as 
(
    select  t1.lat, 
            t1.long, 
            'soybean' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','soybean')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

wheat as 
(
    select  t1.lat, 
            t1.long, 
            'wheat' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','wheat')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

wheat_spring as 
(
    select  t1.lat, 
            t1.long, 
            'wheat_spring' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','wheat_spring')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

),

wheat_winter as 
(
    select  t1.lat, 
            t1.long, 
            'wheat_winter' as crop,
            t1.year,
            t2.country,
            coalesce(t1.yield,0) as yield

    from        {{source('staging','wheat_winter')}}           t1
    left join   {{source('staging','geo_coords')}}      t2 on t1.lat = t2.lat and t1.long = t2.long

)



select * from maize
union all 
select * from maize_major
union all 
select * from maize_second
union all 
select * from rice
union all 
select * from rice_major
union all 
select * from rice_second
union all 
select * from soybean
union all 
select * from wheat
union all 
select * from wheat_spring
union all 
select * from wheat_winter


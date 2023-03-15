select t1.*, t2.country
from {{ source('staging','wheat') }} t1 
left join {{ source('staging','geo_coords') }} t2 on t1.lat = t2.lat and t1.long = t2.long
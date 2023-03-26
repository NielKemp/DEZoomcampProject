# Global Crop Yield Analysis: 1982 - 2015
![alt text](https://www.europeanscientist.com/wp-content/uploads/thumbs/quantifying-photosynthesis-38qhspxd3wtfwicjr2el1c.jpg)

We'll be taking a look at processing annual crop yield data as part of a capstone project for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) offered by [DataTalks.Club](https://datatalks.club/). As part of this proejct we developed and implemented pipelines to process data from webbased sources to cloud based infrastructure and subsequently presented this data in a neat dashboard.

## Problem Description

We used the [Global dataset of historical yields v1.2 and v1.3 aligned version] (https://doi.pangaea.de/10.1594/PANGAEA.909132). This is a dataset that uses various kind of satelite imagery to build datasets of annual crop yields for 10 different crops for countries. In it's raw format the data consists of yield measured in tonnes per hectar for a specific crop for a corresponding longitude/latitude coordinate. The dataset contains data for 10 crops from 1981 to 2016, but due to the first and last years having missing values we'll only consider the data for 1982 to 2015.

The pipeline processes this data from the 720 x 360 entry array in it's native .cf4 format into a deep table with 259,200 rows that contains the following fields (this is done for every crop, for every year between 1982 and 2015): 
* Lat - lattitude coordinate
* Long - longitude coordinate
* Yield - Yield in tonnes per hectar

We then used geocoordinate data from [Natural Earth Data](https://www.naturalearthdata.com/downloads/) to build a lookup table that matches each lat/long coordinate in our processed datasets with a country.

The final dataset we build has yield data for each crop between 1982 and 2015 and has the following fields:
* Lat
* long
* Yield
* Crop
* Country

The final dashboard can be viewed by clicking [HERE](https://lookerstudio.google.com/reporting/b1e71da9-cf1b-4bbd-adb4-71a560e2c2f7)


DataSets: 
    - Yields per year per lat/long: https://doi.pangaea.de/10.1594/PANGAEA.909132
    - Country borders: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/


Terraform
    - command in terminal: terraform init
    - command in terminal: terraform plan -var="project=round-honor-373909"
    - command in terminal: terraform apply
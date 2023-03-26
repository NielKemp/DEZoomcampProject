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

## Technologies used: 
* Cloud: [Google Cloud]
* Infrastructure: [Terraform](https://www.terraform.io/)
* Orchestration: [Prefect](https://www.prefect.io/)
* Data lake: [Google Cloud Storage](https://cloud.google.com/storage)
* Data transformation: [dbt](https://www.getdbt.com/)
* Data warehouse: [Google BigQuery](https://cloud.google.com/bigquery)
* Data visualization: [Google Looker Studio](https://lookerstudio.google.com/u/0/navigation/reporting)


## Run your own copy: 

Before we run our own copy of the pipelines, we need to setup some things

### 1. Google Platform
GCP offers up to 3 months or $300 free, depending on which you hit first. So it's a nice and easy way to dip your toes into cloud computing.
* Create an account [HERE](https://cloud.google.com/free) 
* After registering, create a new project [HERE](https://console.cloud.google.com/cloud-resource-manager)
* Create a service account by clicking [HERE](https://console.cloud.google.com/iam-admin/serviceaccounts)
* Assign the following permissions to the service account you just created:
    * BigQuery Admin
    * Storage Admin
    * Storage Object Admin
* Next we'll create some KEYS by following the setps giver: 
    * Navigate to the following: IAM and Admin -> Service Account -> Keys
    * Click on ADD KEY
    * Generate a new JSON Key
    * Save it somewhere you can easily find later. (NB: Don't share this key with anybody)
* Install the Google SDK by following the instructions found [HERE](https://cloud.google.com/sdk/docs/install-sdk)
* Authenticate the Google SDK and refresh the session token:
```export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login```


Configure Identity and Access Management (IAM) for the service account, giving it the following privileges: BigQuery Admin, Storage Admin and Storage Object Admin


DataSets: 
    - Yields per year per lat/long: https://doi.pangaea.de/10.1594/PANGAEA.909132
    - Country borders: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/


Terraform
    - command in terminal: terraform init
    - command in terminal: terraform plan -var="project=round-honor-373909"
    - command in terminal: terraform apply
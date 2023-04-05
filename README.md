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
* Cloud: [Google Cloud](https://cloud.google.com/)
    * Data lake: [Google Cloud Storage](https://cloud.google.com/storage)
    * Data transformation: [dbt](https://www.getdbt.com/)
    * Data warehouse: [Google BigQuery](https://cloud.google.com/bigquery)
* Infrastructure: [Terraform](https://www.terraform.io/)
* Orchestration: [Prefect](https://www.prefect.io/)
* Analytics Engineering [dbt](https://getdbt.com)
* Data visualization: [Google Looker Studio](https://lookerstudio.google.com/u/0/navigation/reporting)

## Run your own copy: 

Before we run our own copy of the pipelines, we need to setup some things. We'll assume you're using LINUX. 

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
~~~ 

export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login

~~~


### 2. Python Environment

You'll need to be able to execute some python code, and we all know how tricky that can get, so we've gone ahead and packaged all the required packages together, you can use your favorite environment manager in python to create a new environment, and then load the packages in the requirments.txt file. 

An example if you have anacondas installed is: (If you get stuck you can reference the [Anacondas Documentation] (https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) )
* Create a new environment using: ``` conda create --name myenv python=3.9```
* Install pip into the new environment: ``` conda install -n myenv pip ```
* Run some prefect setups: ``` prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api ```
* Activate environment using: ``` conda activate myenv ```
* Install the packages required: ``` pip install -r requirements.txt ```

### 3. Setting up Terraforma and creating Infrastructure

* First, you'll need to download Terraform, and then add the executeable to the BIN directory so you can use the 'Terraform' command from the CLI, to do this run the following CLI commands:
~~~
sudo apt-get install unzip
cd ~/bin
wget https://releases.hashicorp.com/terraform/1.4.1/terraform_1.4.1_linux_amd64.zip
unzip terraform_1.4.1_linux_amd64.zip
rm terraform_1.4.1_linux_amd64.zip
~~~
* Navigate to the Terraform directory containing the main.tf and variables.tf folder
* Execute the following commands using CLI
~~~
terraform init
terraform plan
terraform apply
~~~

### 4. Setting up Orchestration

Prefect should have been installed as part of the environment creation, so this section will focus on setting up the blocks required. 

Start the prefect server by running ``` prefect orion start ```
Once it's up and running you can access the GUI at: http://127.0.0.1:4200/ 
* Note, you may need to setup port forwarding if you're working on a VM. 

You can create blocks [HERE](http://127.0.0.1:4200/blocks)

Take not of where your GCP credentials are stored, you'll need them!

Create the following blocks in Prefect, in order to change less things later on in the code, assign the same names as given in brackets. 
* GCP Credentials (zoom-gcp-creds)
* GCS Bucket (zoom-gcs-block)

### 5. Running the pipeline

Now that everything is set up, you can run the pipeline. 

Execute the files by running the following commands in order, please note it takes quite a long time to run:
* ``` python etl_web_to_gcs.py ```  NOTE: Quite a lot of files, takes an hour or so
* ``` python etl_gcs_to_bq.py ```   NOTE: Quite a lot of files, takes an hour or so
* ``` python etl_map_lkp.py ```     NOTE: This is an extremely long running piece of code, it runs for between 2 and 3 hours!!!
* ``` python etl_map_lkp_bq.py ```  

### 6. Analytics Engineering

In order to recreate the logical tables in Google Big Query, you'll need a dbt account. 

You can sign up [HERE](https:/www.getdbt.com) 

Create a new project, and follow the prompts. After setting up a new project and connecting it with your Google Cloud Platform, navigate to the dbt project saved in this repo: https://github.com/NielKemp/DEZoomcampProject/tree/main/dbt

Clone this repo in your DBT instance, and execute the following commands: 

* ``` dbt build ```
* ``` dbt run ```

It should execute the full path and create the neccessary tables in the required schema. 


### 7. Dashboard

After completing all these steps, you should be able to access the created tables in Big Query. 

These tables were used to create the dashboard that's pictured below, a live version can also be found [HERE](https://lookerstudio.google.com/reporting/b1e71da9-cf1b-4bbd-adb4-71a560e2c2f7)

<img src="/FinDashboard.png">
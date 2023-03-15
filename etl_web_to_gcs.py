from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import netCDF4 as cf
import zipfile
import requests 
import io


@task()
def fetch(dataset_url: str):
    r = requests.get(dataset_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data/yields/")

@task()
def process_c4_data(crop, year):
    ds = cf.Dataset(f'data/yields/{crop}/yield_{year}.nc4')

    data = pd.DataFrame()

    h = ds.variables['var']
    lat = ds.variables['lat']
  
    for i in ds.variables['lon']:
        hs = pd.Series(h[:,i], index = lat)
        hs = hs.reset_index()
        if i > 180:
            i = i -360
        hs['long'] = i
        data = data.append(hs)

    data.rename(columns = {'index':'lat', 0:'yield'}, inplace = True)
    return data

@task()
def write_local(df: pd.DataFrame, dataset_file: str,  year: int, crop: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/yields/{crop}/yield_{year}.parquet")
    df.to_parquet(path, compression="gzip")
    return path     

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs-block")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

#@flow()
def etl_web_to_gcs(year:int, crop:str) -> None:
    """The main ETL function"""
    
          
    print('============================ Downloading Data ============================')

    fetch('https://store.pangaea.de/Publications/IizumiT_2019/gdhy_v1.2_v1.3_20190128.zip')

    print('============================ Download Complete============================')
    print('===================================================================================================')
    dataset_file = f"yield_{year}.parquet"

    print(f'Processing for file:  {dataset_file}')
    print('===================================================================================================')
    print(f'============================ Processing Datafile: {dataset_file} ============================')
    fin_data = process_c4_data(crop, year)
    print(f'============================ Processing Completed: {dataset_file} ============================')
    print('===================================================================================================')
    print(f'============================ Writing {dataset_file} Locally ============================')
    path = write_local(fin_data, dataset_file, year, crop)
    print(f'============================ Writing {dataset_file} Locally Completed ============================')
    print('===================================================================================================')
    print(f'============================ Writing {dataset_file} to GCS bucket ============================')
    write_gcs(path)
    print(f'============================ Writing {dataset_file} to GCS bucket Completed============================')

@flow()
def main_flow(crop:list[str] = ['wheat'],year:list[int] = [1982, 1983, 1984]):
    for crop_ in crop:
        for year_ in year:
            etl_web_to_gcs(year_, crop_)

if __name__ == "__main__":
    year = list(range(1982,2016))
    crop = ['maize', 'maize_major', 'maize_second', 'rice', 'rice_major','rice_second',  'soybean', 'wheat', 'wheat_spring', 'wheat_winter']
    main_flow(crop, year)    



from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import netCDF4 as cf
import zipfile

import geopandas as gpd

from shapely.geometry import Point

import subprocess



@task()
def fetch(dataset_url: str):
    
    process = subprocess.Popen(
           f'wget -P data/ {dataset_url}',
           stdout = subprocess.PIPE,
           stderr = subprocess.PIPE,
           text = True,
           shell = True
       )

    std_out, std_err = process.communicate()

    with zipfile.ZipFile('data/ne_10m_admin_0_countries.zip', 'r') as zip_ref:
            zip_ref.extractall('data/maps/')


@task()
def process_c4_data():
    ds = cf.Dataset(f'data/yields/wheat/yield_2000.nc4')

    data = pd.DataFrame()

    h = ds.variables['var']
    lat = ds.variables['lat']
  
    for i in ds.variables['lon']:
        hs = pd.Series(h[:,i], index = lat)
        hs = hs.reset_index()
        i = i -180
        hs['long'] = i
        data = data.append(hs)

    data.rename(columns = {'index':'lat', 0:'yield'}, inplace = True)
    data.reset_index(inplace = True)
    return data[['lat', 'long']]

@task()
def process_maps(data):

    gdf = gpd.read_file("data/maps/ne_10m_admin_0_countries.shp")

    for index, row in data.iterrows():

        p1 = Point(row['long'], row['lat'])

        for index_,row_ in gdf.iterrows():
            if p1.within(row_.geometry):
                data.loc[index, 'country'] = row_.ADMIN
                country = row_.ADMIN
                print(country)
                print('added')
                break
        print(f'Point: {p1} processed')

    return data


@task()
def write_local(df: pd.DataFrame) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/maps/coord_assign.parquet")
    df.to_parquet(path, compression="gzip")
    return path    

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs-block")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_map_lkp() -> None:
    """The main ETL function"""
    
    fetch('https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip')

    yield_file = process_c4_data()
    
    fin_data = process_maps(yield_file)

    path = write_local(fin_data)
  
    write_gcs(path)
  

@flow()
def main_flow():
    etl_map_lkp()

if __name__ == "__main__":
   main_flow()    
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs( year: int, crop: str) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"/yields/{crop}/yield_{year}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"./data/{gcs_path}")


@task()
def transform(path: Path, year:int) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    df['year'] = year
    return df



@task()
def write_bq(df: pd.DataFrame, crop:str) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table=f"yield_staging.{crop}",
        project_id="round-honor-373909",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq(year, crop):
    """Main ETL flow to load data into Big Query"""
  
    print(f'=================== Loading Yield Data for {crop} in {year} ===================')
    path = extract_from_gcs( year, crop)
    print(f'=================== Data Loaded ===================')

    print(f'=================== Adding Year to File ===================')
    df = transform(path, year)
    print(f'=================== Year Added ===================')
    print(f'=================== Adding data for {year} to {crop} dataset in BQ ===================')
    write_bq(df, crop)
    print(f'=================== Data for {year} to {crop} added to dataset in BQ ===================')


@flow()
def main_flow(years:list[int] = [1,2],crops:list[str] = ['maize']):
    for year in years:
        for crop in crops:
            etl_gcs_to_bq(year, crop)
    print(f'=================== All Yield data loaded to BQ ===================')

if __name__ == "__main__":
    year = list(range(1982,2016))
    crop = ['maize','maize_major', 'maize_second', 'rice', 'rice_major','rice_second',  'soybean', 'wheat', 'wheat_spring', 'wheat_winter']
    #, 
    main_flow(year, crop)    
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs() -> Path:
    """Download trip data from GCS"""
    gcs_path = f"/maps/coord_assign.parquet"
    gcs_block = GcsBucket.load("zoom-gcs-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"./data/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table=f"yield_staging.geo_coords",
        project_id="round-honor-373909",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
  
    print(f'=================== Loading Maps Data ===================')
    path = extract_from_gcs()
    print(f'=================== Data Loaded ===================')

    print(f'=================== Reading parquet file ===================')
    df = transform(path)
    print(f'=================== Data read ===================')
    print(f'=================== Adding map data to BQ===================')
    write_bq(df)
    print(f'=================== Map data added to dataset in BQ ===================')


@flow()
def main_flow():
    
    etl_gcs_to_bq()

    print(f'=================== All Map data loaded to BQ ===================')

if __name__ == "__main__":
    
    main_flow()    
import xarray as xr
from typing import Union

import dask_geopandas
import geopandas as gpd
import xarray as xr

import boto3

import urllib3

urllib3.disable_warnings() ## temporary fix only!

url = "s3://eoepca/wf-ebcf1f96-95b3-11ee-bf3f-0242ac110007/catalog.json"
result_folder_name = url.rsplit("/",1)[0].rsplit("/",1)[1]
bucket_name = url.rsplit("/",1)[0].rsplit("/",1)[0].replace("s3://", "")

# Init S3 session for Creodias
S3_ENDPOINT = f"https://minio.192-168-49-2.nip.io"
session = boto3.session.Session()
s3resource = session.resource('s3', aws_access_key_id="eoepca", aws_secret_access_key="changeme", endpoint_url=S3_ENDPOINT, verify=False)

# s3_response_object = s3resource.Object(bucket_name, "catalog.json")
# print(s3_response_object.get())
#object_content = s3_response_object['Body'].read()

# List bucket contents
bucket = s3resource.Bucket(bucket_name)

for obj in bucket.objects.filter(Prefix=result_folder_name):
    file_name = obj.key.rsplit("/", 1)[1]
    bucket.download_file(obj.key, file_name)
    if file_name.rsplit(".", 1)[1] == "nc":
        dArray = xr.load_dataarray(file_name)

    

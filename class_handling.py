import xarray as xr
from typing import Union

import dask_geopandas
import geopandas as gpd
import xarray as xr

import boto3

url = "s3://eoepca/wf-44d8d3f2-9505-11ee-adcc-0242ac110006/catalog.json"

# Init S3 session for Creodias
S3_ENDPOINT = f"https://minio.192-168-49-2.nip.io"
session = boto3.session.Session()
s3resource = session.resource('s3', aws_access_key_id="eoepca", aws_secret_access_key="changeme", endpoint_url=S3_ENDPOINT, verify=False)

bucket_name = "eoepca"
result_folder_name = "wf-027d6052-9043-11ee-8cb4-0242ac110006"

# List bucket contents
bucket = s3resource.Bucket(bucket_name)

for obj in bucket.objects.filter(Prefix=result_folder_name):
    file_name = obj.key.rsplit("/", 1)[1]
    #with open(file_name, "w") as f:
    bucket.download_file(obj.key, file_name)



raise Exception()

RasterCube = xr.DataArray
VectorCube = Union[gpd.GeoDataFrame, dask_geopandas.GeoDataFrame, xr.Dataset]



cube = RasterCube([1,2,3,4],
                  dims=['time:proc'],
                  coords={'time:proc':[1,2,3,4]})

cube = cube.assign_attrs(units= {"1":1, "2":2}, text = "some text here")
print(cube['time:proc'].values)



cube.attrs['units'] = str(cube.attrs['units'])

print(cube)

cube.attrs['units'] = dict(cube.attrs['units'])

print(cube.attrs['units']['1'])
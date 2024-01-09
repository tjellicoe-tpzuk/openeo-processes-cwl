import xarray as xr
from github import Github
import rioxarray
from datetime import datetime as dt
import time
import os
import requests

#####
# This script is an example of how the data could be prepared before being handed as an input to the the run_cwl_url process.
# The input will be some data, often a raster data cube, but any data type is supported.
# This data will then be placed in an accessible location, either on a remote server (here we use GitHub) or locally on the server, 
# and the location of the file will be returned as a string. 
#####

__all__ = ["cwl_preparation"]

## This function creates a netcdf file, uploads it to a GitHub repository and returns the url location.
def _create_file_url(data: xr.DataArray, git_repository: str, git_token: str):
    g = Github(git_token)
    repo = g.get_repo(git_repository)
    data.attrs['reduced_dimensions_min_values'] = str(data.attrs['reduced_dimensions_min_values'])
    data = _convert_file_format(data)
    outfile = data.to_netcdf()
    timeNow = str(time.time())[-6:]
    fileName = f"openEO_output_{timeNow}"
    try:
        repo.create_file(f'data/{fileName}.nc', 'upload netcdf', outfile, branch='main')
    except:
        print("Something went wrong when saving the file :(")
    #print(repo)
    url = f"https://raw.githubusercontent.com/{git_repository}/main/data/{fileName}.nc"
    
    return url

def _create_file_local(data: xr.DataArray):
    data.attrs['reduced_dimensions_min_values'] = str(data.attrs['reduced_dimensions_min_values'])
    data = _convert_file_format(data)
    outfile = data.to_netcdf()
    out_path = os.getcwd()
    with open("output_file.nc", "wb") as file:
        file.write(outfile)
        out_path = f"{out_path}/output_file.nc"
    file.close()
    return out_path

### Temporary definition only, user must update this function to ensure file is output in correct format
def _convert_file_format(data):
    ### This function is to be completed by the user to ensure the correct output format is used,
    ### As part of this example, and as the snuggs.cwl script requires a STAC input, we will create a STAC catalog to be output

    new_format_data = data

    return new_format_data

## This is a function to be used locally for testing of this function, as the runtime required to run this function is not 
## currently supported on openEO.
def cwl_preparation(data: xr.DataArray, context: dict=None):
    #xarrayTest = data #.to_array()

    save_location = context['save_location']
    git_repository = context['git_repository']
    git_token = context['git_token']

    if save_location == "url":
        if git_repository == None or git_token==None:
            raise Exception("InsufficientArguments", "Please provide Git access token and Git repository location to save to a URL.")
        url = _create_file_url(data, git_repository, git_token)
    elif save_location == "local":
        url = _create_file_local(data)
    else:
        raise Exception("InvalidSaveType", f"Please provide one of 'url' or 'local' to select correct save location, not {save_location}.")
    return url

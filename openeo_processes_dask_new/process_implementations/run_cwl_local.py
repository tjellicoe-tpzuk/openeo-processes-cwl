import os
import requests
import json
import time
import boto3
import urllib3
import xarray as xr
import cwltool.factory
import cwltool.context
import os
import time

#####
# This script will run a CWL script locally and load in the output as a data array for further processing.
#####

__all__ = ["run_cwl_local"]


def save_file(data):
    outPath = os.getcwd()

    try:
        data.attrs['reduced_dimensions_min_values'] = str(data.attrs['reduced_dimensions_min_values'])
    except:
        None
    try:
        data.attrs['spec'] = str(data.attrs['spec'])
    except:
        None
    try:
        data.attrs['processing:software'] = str(data.attrs['processing:software'])
    except:
        None

    outfile = data.to_netcdf()
    outfile_name = f"{outPath}/temp_file.nc"

    with open(outfile_name, "wb") as file:
        file.write(outfile)
    file.close()
    return outfile_name

def rem_file(dataPath):
    os.remove(dataPath)

def run_cwl_local(cwl_location, data, cwl_inputs, context=None):

    dataLocation = save_file(data)

    runtime = cwltool.context.RuntimeContext()
    runtime.outdir = os.getcwd()

    fac = cwltool.factory.Factory(runtime_context=runtime)

    ## Note elsewhere we use file_name: {path: ....}, rather than location, difference here is not currently clear
    inputs = {"input_reference": {
            "location": dataLocation,
            "class": "File"
                }
            }

    inputs.update(cwl_inputs)

    echo = fac.make(cwl_location)
    result = echo(**inputs)

    outData = result['results']['location']
    outData = outData.replace("file://","")
    outData = outData.replace("%20", " ")

    #print(outData)

    rem_file(dataLocation)
        
    files = os.listdir(outData)

    for file in files:
        if file.rsplit(".",1)[1] == "nc":
            filePath = outData + "/" + file
            outData = xr.load_dataset(filePath)

    return outData

# if __name__ == "__main__":
#     ### Complete these lines as required to test the desired files
#     cwlLocation = "https://raw.githubusercontent.com/EOEPCA/deployment-guide/main/deploy/samples/requests/processing/snuggs.cwl"
#     cwlScriptName = "snuggs-0_3_0"
#     inputDataLocation = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
#     inputSExpression = "ndvi:(/ (- B05 B03) (+ B05 B03))"
#     domain = "192-168-49-2.nip.io"
#     ######

#     print(run_cwl_url(domain, cwlLocation, cwlScriptName, inputDataLocation, inputSExpression))

import openeo 
#from openeo import download_results
import json
from openeo.internal.graph_building import PGNode
import sys
from time import sleep
import math
import os
import time
import mimetypes
import datetime as dt

out_dir = os.getcwd()

## this script will take as an input a dataset name for EO data available via Google Earth Engine (https://developers.google.com/earth-engine/datasets/catalog), 
## which it will them compute some complex process using OpenEO in-build processes and return the output STAC catelogue item

testing = True

def main(dataName: str, funcName: str, coords: dict, tempExt: [str], outFileName: str="output_file"):

    outName = outFileName

    print("HERE")
    connection = openeo.connect("https://earthengine.openeo.org")

    connection.authenticate_basic("group11", "test123")

    datacube = connection.load_collection(dataName,
                               spatial_extent=coords,
                               temporal_extent=tempExt,
                               bands=["B4", "B8", "B11"])

    B4 = datacube.band("B4")
    B8 = datacube.band("B8")

    # ## Defining Process Graph Nodes to extract array elements (here bands) and calculate NDVI or NDWI.
    # red = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B4"})
    # nir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B8"})
    # swir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B11"})

    # ndvi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": red}})
    # ndwi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": swir}})

    # if funcName == "ndvi":
    #     datacube = datacube.reduce_dimension(dimension="bands", reducer=ndvi)
    # elif funcName == "ndwi":
    #     datacube = datacube.reduce_dimension(dimension="bands", reducer=ndwi)
    # else:
    #     raise Exception("function not supported (yet!!)", funcName)

    datacube = datacube.save_result(format="netcdf4")
    job = datacube.create_job()
    outputResults = job.start_and_wait()
    outputResults.download_results(f"{out_dir}/{outName}.tif")
    print("To see your results open https://hub.openeo.org/")

 

if __name__ == "__main__":
    if testing:
        dataSet = "COPERNICUS/S2_SR_HARMONIZED"
        funcName = "ndvi"
        coords = {
            "west": -3.33,
            "north": 52.56,
            "east" : 1.25,
            "south" : 50.98
        }
        tempExt = ["2017-06-01", "2017-07-01"]
        outFileName = f"{dataSet}_".replace("/","-") + funcName + "_applied.tiff"
    else:
        args = sys.argv
        dataSet = args[1]
        funcName = args[2]
        n = 3
        coords = {
            "west": float(args[n+3]),
            "north": float(args[n+2]),
            "east" : float(args[n]),
            "south" : float(args[n+1])
        }
        tempExt = [args[7], args[8]]
        outFileName = args[9]
    
    main(dataSet, funcName, coords, tempExt, outFileName)
import openeo 
#from openeo import download_results
import json
from openeo.internal.graph_building import PGNode
import sys
from time import sleep
import math

connection = openeo.connect("openeo.vito.be").authenticate_oidc()


# Load initial data cube.

s2_cube = connection.load_collection(

    "SENTINEL2_L2A",

    spatial_extent={"west": 4.00, "south": 51.04, "east": 4.10, "north": 51.1},

    temporal_extent=["2022-03-01", "2022-03-31"],

    bands=["B02", "B03", "B04"]

)

s2_cube = s2_cube.save_result(format="NETCDF")

result = connection.execute(s2_cube)


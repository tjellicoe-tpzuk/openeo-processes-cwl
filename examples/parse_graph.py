from openeo_pg_parser_networkx import OpenEOProcessGraph

EVI_GRAPH_PATH = "./examples/data/pg-evi-example.json"

parsed_graph = OpenEOProcessGraph.from_file(EVI_GRAPH_PATH)

import importlib
import inspect
import sys
print(sys.path)

from openeo_pg_parser_networkx import ProcessRegistry
from openeo_processes_dask_new.process_implementations.core import process
from openeo_pg_parser_networkx.process_registry import Process

process_registry = ProcessRegistry(wrap_funcs=[process])

# Import these pre-defined processes from openeo_processes_dask and register them into registry
processes_from_module = [
    func
    for _, func in inspect.getmembers(
        importlib.import_module("openeo_processes_dask_new.process_implementations"),
        inspect.isfunction,
    )
]

contents = inspect.getmembers(importlib.import_module("openeo_processes_dask_new.process_implementations"))
print(contents)

specs_module = importlib.import_module("openeo_processes_dask_new.specs")
print(specs_module)
#print((specs_module.filter_temporal))
specs = {}
for func in processes_from_module:
    print(str(func))
    try:
        specs.update({
            func.__name__: getattr(specs_module, func.__name__)
        })
    except:
        print(func.__name__ + " is missing")
        continue

for func in processes_from_module:
    process_registry[func.__name__] = Process(
        spec=specs[func.__name__], implementation=func
    )

# I/O processes aren't generic (yet), therefore have to custom define those. 
def load_collection(id, spatial_extent, temporal_extent, bands = [], properties = {}, **kwargs):
    # No generic implementation available, so need to implement locally!
    import xarray as xr
    return xr.open_dataset("./data/boa.nc").to_array(dim="bands")

#
##
##### to be completed
# I/O processes aren't generic (yet), therefore have to custom define those. 
def load_stac(id, spatial_extent, temporal_extent, bands = [], properties = {}, **kwargs):
    # No generic implementation available, so need to implement locally!
    import xarray as xr
    return None
#####
##
#

def save_result(data, format = 'netcdf', options = None):
    # No generic implementation available, so need to implement locally!
    import xarray as xr
    print(data.attrs['reduced_dimensions_min_values'])
    data.attrs.update({'reduced_dimensions_min_values':f"{data.attrs['reduced_dimensions_min_values']['bands']}"})
    outfile = data.to_netcdf()
    
    with open("output_file.nc", "wb") as file:
        file.write(outfile)
    file.close()

from openeo_processes_dask_new.specs import load_collection as load_collection_spec
from openeo_processes_dask_new.specs import save_result as save_result_spec

process_registry["load_collection"] = Process(spec=load_collection_spec, implementation=load_collection)
process_registry["save_result"] = Process(spec=save_result_spec, implementation=save_result)

pg_callable = parsed_graph.to_callable(process_registry=process_registry)

pg_callable()

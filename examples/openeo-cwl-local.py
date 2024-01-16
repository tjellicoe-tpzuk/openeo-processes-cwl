from openeo_processes_dask_new.process_implementations import (
    run_cwl_local, run_cwl_ades, cwl_preparation
)
import importlib
import inspect
from openeo_pg_parser_networkx import ProcessRegistry
from openeo_processes_dask_new.process_implementations.core import process
from openeo_pg_parser_networkx.process_registry import Process

## First prepare the process registry with all the defined openEO processes in our new back-end
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
#print(contents)

specs_module = importlib.import_module("openeo_processes_dask_new.specs")
#print(specs_module)
#print((specs_module.filter_temporal))
specs = {}
for func in processes_from_module:
    #print(str(func))
    try:
        specs.update({
            func.__name__: getattr(specs_module, func.__name__)
        })
    except:
        #print(func.__name__ + " is missing")
        continue

for func in processes_from_module:
    process_registry[func.__name__] = Process(
        spec=specs[func.__name__], implementation=func
    )


def load_collection(id=None, spatial_extent=None, temporal_extent=None, bands = [], properties = {}, **kwargs):
    # No generic implementation available, so need to implement locally!
    import xarray as xr
    return xr.load_dataset("./data/boa.nc")


def save_result(data, file_name, format = 'netcdf', options = None):
    # No generic implementation available, so need to implement locally!
    import xarray as xr

    outfile = data.to_netcdf()
    
    with open(file_name, "wb") as file:
        file.write(outfile)
    file.close()

from openeo_processes_dask_new.specs import load_collection as load_collection_spec
from openeo_processes_dask_new.specs import save_result as save_result_spec

process_registry["load_collection"] = Process(spec=load_collection_spec, implementation=load_collection)
process_registry["save_result"] = Process(spec=save_result_spec, implementation=save_result)

## Construct and execute process graph

input_cube = load_collection()

## Construct graph with local CWL execution

cwl_location = '../convert-netcdf-basic/convert-nc-app.cwl'
cwl_inputs = {
    "fn": "scale",
    "size": "0.1"
}

## Execute CWL script on given data
output_cube = run_cwl_local(data=input_cube, cwl_location=cwl_location, cwl_inputs=cwl_inputs)
save_result(data=output_cube, file_name="local_output.nc")
## Construct graph with ADES CWL execution

git_token = "INSERT TOKEN HERE",
git_repository = "INSERT GIT REPO HERE of format <user_name>/<repo_name>"

## Upload data to remote server ready for ADES access
cube_url = cwl_preparation(data=input_cube, git_token=git_token, git_repository=git_repository)

cwl_url = "https://raw.githubusercontent.com/tjellicoe-tpzuk/ades_python_convert/main/netcdf_integration/convert-nc-app.cwl"

## replace with own minikube ip
domain = "192-168-49-2.nip.io" 
cwl_inputs = {
    "fn": "scale",
    "size": "0.1"
}

## Execute CWL script on given data via the ADES
output_cube = run_cwl_ades(cwl_url=cwl_url, data=cube_url, domain=domain, cwl_inputs=cwl_inputs)
save_result(data=output_cube, file_name="remote_output.nc")

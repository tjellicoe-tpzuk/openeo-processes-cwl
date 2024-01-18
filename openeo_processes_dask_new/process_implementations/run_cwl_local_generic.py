import os
import xarray as xr
import cwltool.factory
import cwltool.context
import os

#####
# This script will run a CWL script locally and load in the output as a data array for further processing.
#####

__all__ = ["run_cwl_local_generic"]


def run_cwl_local_generic(cwl_location, cwl_inputs, context:dict=None):

    if os.path.isfile(cwl_location) and context:
        raise Exception("CWLStepNameException", f"For a local CWL script you cannot provide a step name, {context}, the 'main' workflow will be run by default. This functionality is to be fixed in future.")



    runtime = cwltool.context.RuntimeContext()
    loadContext = cwltool.context.LoadingContext()
    runtime.outdir = os.getcwd()

    fac = cwltool.factory.Factory(runtime_context=runtime) #, loading_context=loadContext)

    ## Note elsewhere we use file_name: {path: ....}, rather than location, difference here is not currently clear
    inputs = {}

    inputs.update(cwl_inputs)
    step_name = None
    if context:
        step_name = context['step_name'] if 'step_name' in context.keys() else None

    if not step_name:
        tool = fac.make(f"{cwl_location}")
    else:
        tool = fac.make(f"{cwl_location}#{step_name}")

    #tool = fac.make(f"{cwl_location}")
    #tool = cwltool.load_tool.load_tool(f"{cwl_location}#snuggs")
    #step = fac.get_step(tool, stepName)

    #result = fac.make_outputs(step.tool.outputs, step.collect_outputs())

    result = tool(**inputs)

    outData = result['results']['location']
    outData = outData.replace("file://","")
    outData = outData.replace("%20", " ")

    #print(outData)
        
    files = os.listdir(outData)

    for file in files:
        if file.rsplit(".",1)[1] == "nc":
            filePath = outData + "/" + file
            outData = xr.load_dataset(filePath)

    return outData

if __name__ == "__main__":

    cwl_inputs = {
        "input_reference": ["https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"],
        "s_expression": ["ndvi:(/ (- B05 B03) (+ B05 B03))"]
    }
    context = {}
    ## For local cwl scripts, no need to provide a step name, but the workflow id must be "main"
    run_cwl_local_generic("/home/tjellicoe/Documents/EOEPCA-and-OPENEO/Git Testing/openeo-processes-cwl/examples/data/snuggs.cwl", cwl_inputs)

    ## For remote cwl scripts you need to provide the step name of the workflow you wish to run, otherwise it will be run with "main"
    #step_name = "snuggs"

    ## This variable is passed in via the context dictionary
    #context = {}
    #context['step_name'] = step_name

    #run_cwl_local_generic("https://raw.githubusercontent.com/EOEPCA/deployment-guide/main/deploy/samples/requests/processing/snuggs.cwl", cwl_inputs, context)

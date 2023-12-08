import os
import requests
import json
import time

import urllib3
urllib3.disable_warnings() ## temporary fix only!

#####
# This script will interface directly with the API provided via the ADES running on a deployeed EOEPCA application package. 
# It allows the entire EOEPCA  processing pipeline to be run from a single Python script, taking the input CWL and input data, and returning
# the location of the final output as a string. Here the output file will be located in a Min.io bucket.
#####

__all__ = ["run_cwl_url"]

base = "https://"
#domain = "192-168-49-2.nip.io"
user = "eric"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def listProcesses(ades):
    ### List processes
    apiQuestion = base + ades + "/" + user + "/wps3/processes"

    print(apiQuestion)

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def deployProcess(ades, cwlLocation):
    ### Deploy Process
    

    apiQuestion = base + ades + "/" + user + "/wps3/processes"

    apiHeader = {'Accept': 'application/json',
                'Content-Type': 'application/json'}

    apiParams = {
        "executionUnit": {
            "href": f"{cwlLocation}",
            "type": "application/cwl"
        }
    }

    rawAnswer = requests.post(apiQuestion, headers=apiHeader, verify=False, json=apiParams) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    print(rawAnswer.headers)

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def getDeployStatus(deployStatus, ades):
    ### Get Deploy Status

    apiQuestion = base + ades + deployStatus

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def executeProcess(ades, cwlScriptName, inputDataLocation, inputSExpression):
    ### Get Execute Status

    

    apiQuestion = base + ades + "/" + user + "/wps3/processes/" + cwlScriptName + "/execution"

    apiHeader = {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Prefer': 'respond-async'}
    
    apiParams = {
        "inputs": {
            "input_reference": inputDataLocation,
            "s_expression": inputSExpression
        },
        'response': 'raw'
    }

    rawAnswer = requests.post(apiQuestion, headers=apiHeader, verify=False, json=apiParams) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))


def getExecuteStatus(executeStatus, ades):
    ### Get Execute Status
    apiQuestion = base + ades + executeStatus

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def getProcessingResults(executeStatus, ades):
    ### Get Processing Results
    apiQuestion = base + ades + executeStatus + "/result"

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

def run_cwl_url(domain: str, cwl_url: str, data: str, cwl_inputs: str):
    ades = f"ades-open.{domain}"
    login = f"auth.{domain}"

    #listProcesses(ades)

    deployProcessRtrn = deployProcess(ades, cwl_url)
    deployStatus = deployProcessRtrn.headers['Location']

    cwlScriptName = deployProcessRtrn.json()['id']

    #getDeployStatus(deployStatus, ades)

    executeStatus = executeProcess(ades, cwlScriptName, data, cwl_inputs).headers['Location']

    status = getExecuteStatus(executeStatus, ades).json()['status']
    print(f"Initial status is {bcolors.OKGREEN + status.upper() + bcolors.ENDC} please wait for processing to finish")
    while status == "running":
        #time.sleep(10)can I bold
        status = getExecuteStatus(executeStatus, ades).json()['status']
        #print(status)
        #print(getExecuteStatus(executeStatus, ades).json())

    if status == "successful":
        ## Return location of minio data catalogue
        out_location = getProcessingResults(executeStatus, ades).json()['StacCatalogUri'] ## = "s3://eoepca/wf-9e9adfb8-9364-11ee-b004-0242ac110006/catalog.json"
        return out_location

    if status == "failed":
        message = getExecuteStatus(executeStatus, ades).json()['message']
        print("Exception raised, message is " + message)
        return False



# if __name__ == "__main__":
#     ### Complete these lines as required to test the desired files
#     cwlLocation = "https://raw.githubusercontent.com/EOEPCA/deployment-guide/main/deploy/samples/requests/processing/snuggs.cwl"
#     cwlScriptName = "snuggs-0_3_0"
#     inputDataLocation = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
#     inputSExpression = "ndvi:(/ (- B05 B03) (+ B05 B03))"
#     domain = "192-168-49-2.nip.io"
#     ######

#     print(run_cwl_url(domain, cwlLocation, cwlScriptName, inputDataLocation, inputSExpression))

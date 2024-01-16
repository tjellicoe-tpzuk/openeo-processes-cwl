## A duplicate of the convert.sh file, but this time written in Python.
#  Depending on success here, this will inform potential to include OpenEO commands within the EOEPCA application package

from PIL import Image
import math
import sys
import requests
from io import BytesIO
import PIL.ImageOps
import os
import json
import time
import datetime as dt
import mimetypes
import xarray as xr

out_dir = os.getcwd()

## function to determine function to be done, here only resize or invert
def do_func(args): # input is --fn invert --url "url" --size "ss"
    func = args[1]
    #print(func)
    if func == "resize":
        ##call resize func
        convert_get_type(args)
    elif func == "invert":
        ##call invert func
        invert_get_type(args)
        #convert_get_type(args)
    elif func == "scale":
        ##call scale function
        scale_get_type(args)
    else:
        raise Exception('This function is not supported in current implementation', func)


## function to determine whether url or stac object to be converted
def convert_get_type(args):
    srcType = args[2]
    size = args[4]
    if srcType == "--url":
        input_file = args[3]
        convert_url(input_file, size)
    elif srcType == "--stac":
        input_dir = args[3]
        convert_stac(input_dir, size)
    elif srcType == "--file":
        input_file = args[3]
        convert_file(input_file, size)
    else:
        raise Exception()

## function to determine whether url or stac object to be converted
def scale_get_type(args):
    srcType = args[2]
    size = args[4]
    if srcType == "--url":
        input_file = args[3]
        scale_url(input_file, size)
    elif srcType == "--stac":
        print("STAC not yet supported")
    elif srcType == "--file":
        input_file = args[3]
        scale_file(input_file, size)
    else:
        raise Exception()

## function to determine whether url or stac object to be inverted
def invert_get_type(args):
    srcType = args[2]
    if srcType == "--url":
        #invert_url(args)
        f = open(f"invert {srcType}.png", "w")
        #f.write("hello world")
        f.close()
    elif srcType == "--stac":
        #invert_stac(args)
        f = open("invert {srcType}.png", "w")
        #f.write("hello world")
        f.close()
    elif srcType == "--file":
        #invert_file(args)
        f = open("invert {srcType}.png", "w")
        #f.write("hello world")
        f.close()
    else:
        raise Exception()

## Take url of netcdf file and apply scaling by 0.001 to each pixel
def convert_url(url_name:str, size:str):
    domainName = os.path.dirname(url_name)
    outName = url_name.replace(domainName + "/", "")
    #outName = outName.replace(".", f"scaled_by_{size}-NEW.")
    outName = outName.replace(".", "-NEW.")
    #fileType = os.path.splitext(url_name)

    response = requests.get(url_name)

    with Image.open(BytesIO(response.content)) as im:
        out_size = percent_to_num(size)
        out_size_tuple = size_to_tuple_url(url_name, out_size)
        out_im = im.resize(out_size_tuple)
        out_im.save(f"{out_dir}/{outName}")
    #createStacItem(outName.replace(".png", ""), ".png")
    #createStacCatalogRoot(outName.replace(".png", ""))

## Take url of netcdf file and apply scaling by 0.001 to each pixel
def scale_url(url_name:str, scale:str):
    domainName = os.path.dirname(url_name)
    outName = url_name.replace(domainName + "/", "")
    #outName = outName.replace(".", f"scaled_by_{size}-NEW.")
    outName = outName.replace(".", "-NEW.")
    #fileType = os.path.splitext(url_name)

    response = requests.get(url_name)

    darray = xr.load_dataarray(response.content)
    temp_attr = darray.attrs

    darray = darray * float(scale)
    
    darray.attrs = temp_attr

    outfile = darray.to_netcdf()
    
    with open(f"{out_dir}/{outName}", "wb") as file:
        file.write(outfile)
    file.close()
    
    #createStacItem(outName.replace(".nc", ""), ".nc")
    #createStacCatalogRoot(outName.replace(".nc", ""))


def scale_file(file_name:str, scale:str):
    #outName = outName.replace(".", f"scaled_by_{size}-NEW.")
    outName = file_name.replace(".", "-NEW.")
    dirName = os.path.dirname(file_name)
    outName = file_name.replace(dirName, "")
    #print(outName)
    dSet = xr.load_dataset(file_name)

    dSetKeys = list(dSet.keys())

    pattern = "B0"

    dSetKeys = [key for key in dSetKeys if pattern in key]

    for key in dSetKeys:
        dSet[key].values = dSet[key].values * float(scale)

    outfile = dSet.to_netcdf()
    
    with open(f"{out_dir}/{outName}", "wb") as file:
        file.write(outfile)
    file.close()
   
    #createStacItem(outName.replace(".nc", ""), ".nc")
    #createStacCatalogRoot(outName.replace(".nc", ""))

def convert_stac(file_dir:str, size:str):

    ## open file directory
    catFileLocation = open(file_dir + "/catalog.json")
    ## open catalog.json
    #print(fileLocation)
    jsonFile = json.load(catFileLocation)
    
    ## identify href of links, .rel object
    fileName = -1
    for i in range(len(jsonFile['links'])):
        print(jsonFile['links'][i])
        if jsonFile['links'][i]['rel'] == "item":
            fileName = [jsonFile['links'][i]['href']]
            break
    ## take file name obtained from above .rel link
    print(fileName)
    if fileName == -1:
        raise Exception("Required JSON file not found in directory", file_dir)
    
    ## identify, via href, the final png to be editted
    jsonFileLocation = open(file_dir + "/" + fileName[0])
    jsonFile = json.load(jsonFileLocation)
    fileName = jsonFile['assets']['logo']['href']
    print(fileName)

    #outName = fileName.replace(".", f"scaled_by_{size}-NEW.")
    outName = outName.replace(".", "-NEW.")
    imgFileLocation = file_dir + "/" + fileName
    ## convert file as before, then update STAC data in JSON (new function for this)

    with Image.open(imgFileLocation) as im:
        out_size = percent_to_num(size)
        out_size_tuple = size_to_tuple_file(imgFileLocation, out_size)
        out_im = im.resize(out_size_tuple)
        print("here " + outName)
        out_im.save(out_dir + "/" + outName)
    #createStacItem(outName.replace(".png", ""), ".png")
    #createStacCatalogRoot(outName.replace(".png", ""))

def convert_file(file_name:str, size:str):
    print("HERE")
    dirName = os.path.dirname(file_name)
    outName = file_name.replace(dirName + "/", "")
    #outName = outName.replace(".", f"_scaled_by_{size}-NEW.")
    outName = outName.replace(".", "-NEW.")
    with Image.open(file_name) as im:
        #im.show("Orignal Image")
        out_size = percent_to_num(size)
        out_size_tuple = size_to_tuple_file(file_name, out_size)
        out_im = im.resize(out_size_tuple)
        print("here " + outName)
        #outName = "outimage.png"
        out_im.save(f"{out_dir}/{outName}")
    #createStacItem(outName.replace(".png", ""), ".png")
    #createStacCatalogRoot(outName.replace(".png", ""))

def invert_file(file_name:str, size:str):

    with Image.open(file_name) as im:
        #im.show("Orignal Image")
        out_im = PIL.ImageOps.invert(im)
    return out_im


## Need to remove ".png" from end of outName
def createStacItem(outName, extension) :
    now = time.time_ns()/1_000_000_000
    dateNow = dt.datetime.fromtimestamp(now)
    dateNow = dateNow.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"
    size = os.path.getsize(f"{outName}{extension}")
    mime = mimetypes.guess_type(f"{outName}{extension}")[0]
    data = {"stac_version": "1.0.0",
  "id": f"{outName}-{now}",
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [-180, -90],
        [-180, 90],
        [180, 90],
        [180, -90],
        [-180, -90]
      ]
    ]
  },
  "properties": {
    "created": f"{dateNow}",
    "datetime": f"{dateNow}",
    "updated": f"{dateNow}"
  },
  "bbox": [-180, -90, 180, 90],
  "assets": {
    f"{outName}": {
      "type": f"{mime}",
      "roles": ["data"],
      "href": f"{outName}{extension}",
      "file:size": size
    }
    },
  "links": [{
    "type": "application/json",
    "rel": "parent",
    "href": "catalog.json"
  }, {
    "type": "application/geo+json",
    "rel": "self",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "root",
    "href": "catalog.json"
  }]
}
    with open(f"{out_dir}/{outName}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def createStacCatalogRoot(outName) :
    data = {
  "stac_version": "1.0.0",
  "id": "catalog",
  "type": "Catalog",
  "description": "Root catalog",
  "links": [{
    "type": "application/geo+json",
    "rel": "item",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "self",
    "href": "catalog.json"
  }]
}
    with open(f'{out_dir}/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

## Convert input size string to a double - removing percentage
def percent_to_num(percentage:str):
    
    if percentage.find("%") == -1:
        raise Exception("Size input is not a percentage, please ensure input ends in '%'")
    else:
        percentage = percentage.replace("%","")
        return float(percentage)


def size_to_tuple_file(file_name:str, size:float):
    image = Image.open(file_name)
    curr_size = image.size
    #print(curr_size)

    #new_size = []
    scale_factor = size/100 ## note, this reduces image size both in the width and height directions

    new_size = [int(math.ceil(x*scale_factor)) for x in curr_size]
    #print(new_size)

    return new_size

def size_to_tuple_url(url_name:str, size:float):
    response = requests.get(url_name)
    image = Image.open(BytesIO(response.content))
    curr_size = image.size
    #print(curr_size)

    #new_size = []
    scale_factor = size/100 ## note, this reduces image size both in the width and height directions

    new_size = [int(math.ceil(x*scale_factor)) for x in curr_size]
    print(new_size)

    return new_size


def convert_main(args: [str]):
    if len(args) == 1:
        raise Exception("no arguments provided, please provide file_name and increase_size")
    file_name = args[1]
    file_name_no_ext = args[1].replace(".png", "")
    increase_size = args[2]
    do_func(args)#.save(f"{file_name_no_ext} resized to {increase_size}.png")

if __name__ == "__main__":
    convert_main(sys.argv)




#convert_image("logo6_med.original-resize.png", "10%")
# increase_size = "200%"

# response = requests.get("https://eoepca.org/media_portal/images/logo6_med.original.png")
# img = Image.open(BytesIO(response.content)).save("test image.png")


# convert_image("https://eoepca.org/media_portal/images/logo6_med.original.png", increase_size).save(f"resized image {increase_size}.png")


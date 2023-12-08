import os
import urllib.request
from tempfile import TemporaryDirectory

#####
# This is a prototype script based on a script from https://pystac.readthedocs.io/en/latest/tutorials/how-to-create-stac-catalogs.html, to investigate 
# how we can convert datacube data from openEO into a STAC catalog that is suitable for EOEPCA processing.
#####


tmp_dir = TemporaryDirectory()
img_path = os.path.join(tmp_dir.name, "image.tif")


url = (
    "https://spacenet-dataset.s3.amazonaws.com/"
    "spacenet/SN5_roads/train/AOI_7_Moscow/MS/"
    "SN5_roads_train_AOI_7_Moscow_MS_chip996.tif"
)
urllib.request.urlretrieve(url, img_path)
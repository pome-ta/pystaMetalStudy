from pathlib import Path
from objc_util import ObjCClass, ObjCInstance, nsurl, load_framework


load_framework('ModelIO')


root = Path('./Resources/')
url = root / Path('./Farmhouse.obj')
out = root / Path('./out.obj')


MDLAsset = ObjCClass('MDLAsset').new()

asset = MDLAsset.initWithURL_(nsurl(str(url)))

asset.exportAssetToURL_(nsurl(str(out)))


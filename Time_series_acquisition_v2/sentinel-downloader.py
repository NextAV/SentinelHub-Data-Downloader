from sentinelhub import SHConfig
import datetime
import time
import pymp
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)


client_id = '758ff8a3-3d39-44cd-8a48-d54ec69da99e'
client_secret = '6MA||#*6&;li)cAdCGRxVYG76DF<0TD}UH|DNSq>'
config = SHConfig()

if client_id and client_secret:
  config.sh_client_id = client_id
  config.sh_client_secret = client_secret

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")



salt_coords_wgs84 = [
  10.849685,
  33.315324,
  11.081773,
  33.452355
]
resolution = 10
salt_bbox = BBox(bbox=salt_coords_wgs84, crs=CRS.WGS84)
salt_size = bbox_to_dimensions(salt_bbox, resolution=resolution)


evalscript_ndsi = """
////VERSION=3 (auto-converted from 1)
// MODIS Normalized Difference Salinity Index (NDSI)
// https://www.indexdatabase.de/db/si-single.php?rsindex_id=57=&sensor_id=14


let viz = ColorGradientVisualizer.createWhiteGreen(-0.89, 0.89);

function evaluatePixel(samples) {
    let val = index(samples.B06, samples.B07);
    return [...viz.process(val),samples.dataMask];
}

function setup() {
  return {
    input: [{
      bands: [ "B06", "B07", "dataMask" ]
    }],
    output: { bands: 4 }  }
}
"""
start_date = datetime.date(2020, 4, 2)
end_date = datetime.date(2021, 5, 1)
r = (end_date - start_date).days + 1

with pymp.Parallel(r) as p:
  for n in p.range(1,r):
    date1 = start_date + datetime.timedelta(n)
    date2 = start_date + datetime.timedelta(n+1)
    request_code = SentinelHubRequest(
      data_folder="dir_ndsi100",
      evalscript=evalscript_ndsi,
      input_data=[
          SentinelHubRequest.input_data(
              data_collection=DataCollection.MODIS,             
              time_interval=(date1, date2),
          )
      ],
      responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
      bbox=salt_bbox,
      size=salt_size,
      config=config,
    )

  #print( "TIFF file with all needed bands was saved \n")
  #Saving your img'bounds': {'bbox': [10.849685, 33.315324, 11.081773, 33.452355],
    
    result_imgs = request_code.get_data(save_data=True)
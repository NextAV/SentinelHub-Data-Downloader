import os
import json
import shutil
x = os.listdir('/home/aymen/Desktop/code sentinel downloader/dir_ndsi')
print(x)

for i in x :
  path='/home/aymen/Desktop/code sentinel downloader/dir_ndsi/'+i+'/request.json'
  path1 = '/home/aymen/Desktop/code sentinel downloader/dir_ndsi/'+i+'/response.tiff'
  f = open(path)
  data = json.load(f)
  s=str(data['request']['payload']['input']['data'])
  name=s.split("'")[7].split('T')[0]
  print(name)
  #new_name = name + 'tiff'
  dst='/home/aymen/Desktop/code sentinel downloader/dataset2/'+name+'.png'
  shutil.copyfile(path1, dst)

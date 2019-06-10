
# importing the requests library 
import requests 
import json
import time
import os
import pprint
import hashlib
from config import *

def sync2server():
	for f in os.listdir(OUTPUT_DIR):
		if f.endswith(".mp4"):
			print('\n\n[INFO]: Syncing %s with server...'%f)
			vid = f
			vid_json = f[:f.index(".mp4")] + '.json'
			postjson(vid_json,vid)
			time.sleep(1)

def postjson(jsonfile,vidname):
	# defining the api-endpoint  
	API_ENDPOINT = "http://%s:%d/question/add" %(API_HOST,API_PORT)
	# sending post request and saving response as response object
	
	with open(OUTPUT_DIR+jsonfile) as json_file:
		json_data = json.load(json_file) 
		json_data1=json.dumps(json_data)
	# print(json_data1)
	headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}

	try:
		r = requests.post(url = API_ENDPOINT, data=json_data1,headers=headers)
	except:
		print('[ERROR]: Unable to communicate with the server!')
		return

	# extracting response text  
	response_text = r.text
	response_json=json.loads(response_text)
	print("[INFO]: response:")
	pprint.pprint(response_json)
	if "uploadStatus" in response_json and response_json["uploadStatus"] == "Successful":
		id = response_json['id']
		files = {'file': ('%s.mp4'%id,open(OUTPUT_DIR+vidname, 'rb'),'video/mp4')}
		original_hash = hashlib.md5(open(OUTPUT_DIR+vidname, 'rb').read()).hexdigest()
		time.sleep(1)
		response = requests.post("http://%s:%d/question/add/%s"%(API_HOST,API_PORT,id), files=files)
		print("\n[INFO]: response:")
		response_json = json.loads(response.text)
		pprint.pprint(response_json)
		if "fileDownloadUri" in response_json:
			#video upload was successful, now video and json can now be deleted
			os.system('rm -f %s%s'%(OUTPUT_DIR,jsonfile))
			os.system('rm -f %s%s'%(OUTPUT_DIR,vidname))
			print('[INFO]: deleted %s and %s from local file system\n'%(jsonfile,vidname))
		else:
			print('[ERROR]: failed to upload video for id %s'%id)
	else:
		print('[ERROR]: failed to post json for %s'%jsonfile)

	

   
   

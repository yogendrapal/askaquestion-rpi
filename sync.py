
# importing the requests library 
import requests 
import json
import time
import os

def sync2server():
	for f in os.listdir("output/"):
		if f.endswith(".mp4"):
			print('\n\n[INFO]: Syncing %s with server...'%f)
			vid = f
			vid_json = f[:f.index(".mp4")] + '.json'
			postjson(vid_json,vid)
			time.sleep(1)

def postjson(jsonfile,vidname):
	# defining the api-endpoint  
	API_ENDPOINT = "http://localhost:8081/question/add"
	# sending post request and saving response as response object
	
	with open("output/"+jsonfile) as json_file:
		json_data = json.load(json_file) 
		json_data1=json.dumps(json_data)
	# print(json_data1)
	headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	r = requests.post(url = API_ENDPOINT, data=json_data1,headers=headers)

	# extracting response text  
	response_text = r.text
	print("[INFO]: response:\n",response_text)
	response_json=json.loads(response_text)
	if "uploadStatus" in response_json and response_json["uploadStatus"] == "Successful":
		id = response_json['id']
		files = {'file': ('%s.mp4'%id,open("output/"+vidname, 'rb'),'video/mp4')}
		time.sleep(1)
		response = requests.post("http://localhost:8081/question/add/%s"%id, files=files)
		print("\n[INFO]: response:\n",response.text)
		response_json = json.loads(response.text)
		if "fileDownloadUri" in response_json:
			#video upload was successful, now video and json can be deleted
			os.system('rm -f output/%s'%jsonfile)
			os.system('rm -f output/%s'%vidname)
			print('[INFO]: deleted %s and %s from local file system'%(jsonfile,vidname))
		else:
			print('[ERROR]: failed to upload video for id %s'%id)
	else:
		print('[ERROR]: failed to post json for %s'%jsonfile)

	

   
   

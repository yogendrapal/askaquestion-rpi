
# importing the requests library 
import requests 
import json
import time
import os
import pprint
import hashlib
from config import *
from logger import json_post_success,video_post_success,check_json_post_status,get_posted_qids

def sync2server():
	for f in os.listdir(OUTPUT_DIR):
		extns = [".mp4",".avi"]
		for e in extns:
			if f.endswith(e):
				print('\n\n[INFO]: Syncing %s with server...'%f)
				vid = f
				vid_json = f[:f.index(e)] + '.json'
				post_status = check_json_post_status(vid)
				if post_status != False:
					print('\n[INFO]: JSON already posted, id = %s' % post_status)
					postvideo(vid_json,vid,post_status)
				else:
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
		print('[ERROR]: Unable to communicate with the server! Please ensure that HOST & PORT are properly configured in config.py.\n')
		return

	# extracting response text  
	response_text = r.text
	response_json=json.loads(response_text)
	print("[INFO]: response:")
	pprint.pprint(response_json)
	if "uploadStatus" in response_json and response_json["uploadStatus"] == "Successful":
		id = response_json['id']
		if json_post_success(vidname,id):
			postvideo(jsonfile,vidname,id)
	else:
		print('[ERROR]: failed to post json for %s'%jsonfile)

def postvideo(jsonfile,vidname,id):
	try:
		ext = vidname.split('.')[-1]
	except:
		ext = ''
	files = {'file': ('%s.%s'%(id,ext),open(OUTPUT_DIR+vidname, 'rb'),'video/%s'%ext)}
	original_hash = hashlib.md5(open(OUTPUT_DIR+vidname, 'rb').read()).hexdigest()
	time.sleep(1)
	response = requests.post("http://%s:%d/question/add/%s"%(API_HOST,API_PORT,id), files=files)
	print("\n[INFO]: response:")
	response_json = json.loads(response.text)
	pprint.pprint(response_json)
	print('\n--MD5--')
	print('Actual MD5:\t' + original_hash)
	print('Response MD5:\t' + response_json['md5']+'\n')
	if "fileDownloadUri" in response_json and response_json['md5'] == original_hash:
		#video upload was successful, now video and json can now be deleted
		if video_post_success(vidname,id):
			os.system('rm -f %s%s'%(OUTPUT_DIR,jsonfile))
			os.system('rm -f %s%s'%(OUTPUT_DIR,vidname))
			
			print('[INFO]: deleted %s and %s from local file system\n'%(jsonfile,vidname))
	else:
		print('[ERROR]: failed to upload video for id %s'%id)

def fetch_posted_questions():
	idlist = get_posted_qids()
	print(idlist)
	#now check each of the id on the server for answer
	#for every available answer we will have to fetch the answer video
	#then delete entry from video_sent table and add entry to answer_received table
   

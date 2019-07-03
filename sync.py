
# importing the requests library 
import requests 
import json
import time
import os
import pprint
import hashlib
from config import *
from logger import json_post_success,video_post_success,check_json_post_status,get_posted_qids, get_remote2local_dict, answer_get_success

def sync2server():
	fetch_posted_questions()
	for f in os.listdir(OUTPUT_DIR):
		extns = [".mp4",".avi"]
		for e in extns:
			if f.endswith(e):
				if f == e:
					continue
				print('\n\n[INFO]: Syncing %s with server...'%f)
				try:
					vid = f
					vid_json = f[:f.index(e)] + '.json'
					post_status = check_json_post_status(vid)
					if post_status != False:
						print('\n[INFO]: JSON already posted, id = %s' % post_status)
						if not postvideo(vid_json,vid,post_status):
							return False
					else:
						if not postjson(vid_json,vid):
							return False
					time.sleep(1)
				except Exception as esync:
					print(esync)
					continue
	return True


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
		return False

	# extracting response text  
	response_text = r.text
	response_json=json.loads(response_text)
	print("[INFO]: response:")
	pprint.pprint(response_json)
	if "uploadStatus" in response_json and response_json["uploadStatus"] == "Successful":
		id = response_json['id']
		if json_post_success(vidname,id):
			return postvideo(jsonfile,vidname,id)
	else:
		print('[ERROR]: failed to post json for %s'%jsonfile)
		return False

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
			#below line is added temporarily to play the question video as the answer
			os.system('cp -f %s%s %s%s'%(OUTPUT_DIR,vidname,ANSWER_DIR,vidname))
			#remove the above line after the answer fetching mechanism is built
			os.system('rm -f %s%s'%(OUTPUT_DIR,jsonfile))
			os.system('rm -f %s%s'%(OUTPUT_DIR,vidname))
			
			print('[INFO]: deleted %s and %s from local file system\n'%(jsonfile,vidname))
			return True
		else:
			return False
	else:
		print('[ERROR]: failed to upload video for id %s'%id)
		return False

def fetch_posted_questions():
	idlist = get_posted_qids()
	r2l = get_remote2local_dict()
	print(idlist)
	for qid in idlist:
		API_ENDPOINT = "http://%s:%d/answer/%s" %(API_HOST,API_PORT,qid)
		r = requests.get(API_ENDPOINT,allow_redirects=True)
		# print(r)
		lid = r2l[qid]
		if not r.status_code == 404:
			print("[INFO]: Saving answer video for local_qid = %s\n"%lid)
			os.system("cd %s && rm -f %s*"%(ANSWER_DIR,lid))
			open(ANSWER_DIR + lid,'wb').write(r.content)
			answer_get_success(lid)

	#now check each of the id on the server for answer
	#for every available answer we will have to fetch the answer video
	#then delete entry from video_sent table and add entry to answer_received table
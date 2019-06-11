import json
from datetime import datetime
from config import *


# log_db = {
# 	'vidname':'temp.mp4',
# 	'date':'',
# 	'time':'',
# 	'machine_id':''
# }


'''
useful links

https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
https://www.programiz.com/python-programming/datetime/current-datetime

'''

def new_log_entry(filename):
	now = datetime.now()
	ldb = {}
	ldb['name'] = filename
	ldb['date'] = now.strftime("%d/%m/%y")
	ldb['time'] = now.strftime("%H:%M:%S")
	ldb['machine_id'] = MACHINE_ID

	#add the json extension
	jsonfile = filename + '.json'
	vidname=filename+ '.mp4'
	with open(OUTPUT_DIR+jsonfile,'w+') as outfile:
		json.dump(ldb,outfile)	
	return

def json_post_success(vidname,id):
	try:
		with open(UNDER_PROCESS_JSON_PATH) as json_file:
			json_data = json.load(json_file)
	except:
		json_data = {}
	json_data[vidname] = id
	with open(UNDER_PROCESS_JSON_PATH,'w+') as outfile:
		json.dump(json_data,outfile)

def video_post_success(vidname,id):
	with open(UNDER_PROCESS_JSON_PATH) as json_file:
		json_data = json.load(json_file)
	del json_data[vidname]
	with open(UNDER_PROCESS_JSON_PATH,'w+') as outfile:
		json.dump(json_data,outfile)
	try:
		with open(VIDEO_SENT_JSON_PATH) as json_file:
			json_data = json.load(json_file)
	except:
		json_data = []
	new_entry = {'id':id}
	json_data.append(new_entry)
	with open(VIDEO_SENT_JSON_PATH,'w+') as outfile:
		json.dump(json_data,outfile)		

def check_json_post_status(vidname):
	try:
		with open(UNDER_PROCESS_JSON_PATH) as json_file:
			json_data = json.load(json_file)
	except:
		return False
	if vidname in json_data:
		return json_data[vidname]
	else:
		return False



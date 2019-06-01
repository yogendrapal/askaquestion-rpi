from config import *
import logger
import record
import random
import post_request


avr = record.AV_Recorder()

while True:
	print('1. Start Recording')
	print('2. Stop Recording')
	print('3. Sync to Server')
	print('4. Exit')
	ch = int(input())
	
	if ch == 1:
		fname = 'vid' + str(random.randint(100,1001))
		avr.record('output/'+fname)
	elif ch == 2:
		avr.stop()
		logger.new_log_entry(fname)
		print('Video was saved as "'+fname + '.mp4"\nPress any key to post video to API..')
		input()
		post_request.postjson(fname+'.json',fname+'.mp4')
	else:
		break


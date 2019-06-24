from config import *
import logger
import record
import random
import sync
import os
import facerec
import uuid


avr = record.AV_Recorder()
fe = None

while True:
	print('1. Start / Stop Recording')
	print('2. Cancel Recording')
	print('3. Sync to Server')
	print('4. ID-List of Sent Videos')
	print('5. Get my question id')
	print('6. Clear Database')
	print('7. Exit')
	ch = int(input())
	
	if ch == 1:
		if avr.is_recording():
			avr.stop()
			logger.new_log_entry(fname,avr.ext)
			facerec.store_face_encodings(fe, fname)
			print('Video was saved as "'+fname + '.' + avr.ext +'"\n')
		else:
			#fname does not include the extension
			fname = str(uuid.uuid4())
			print('Please wait for the system to register your face...')
			fe = facerec.generate_face_encodings()
			if fe:
				avr.record(OUTPUT_DIR+fname)
			else:
				print('No face was found! Recording discarded!\n')
	elif ch == 2:
		avr.discard()
	elif ch == 3:
		sync.sync2server()
	elif ch == 4:
		sync.fetch_posted_questions()
	elif ch == 5:
		print('Please look into the camera...')
		resfid = facerec.fetch_fid()
		if resfid:
			print('Match Found: ',resfid)
		else:
			print('No Match Found')
	elif ch==6:
		os.system('rm -f %s'%DB_PATH)
		os.system('rm -f %s'%FACE_ENCS_NPZ_PATH)
#--these are for testing purposes--
	elif ch==91:
		fe = facerec.generate_face_encodings()
		facerec.store_face_encodings(fe, 'tg')
	elif ch==92:
		resfid = facerec.fetch_fid()
		if resfid:
			print('Match Found: ',resfid)
		else:
			print('No Match Found')
	elif ch==93:
		print(logger.get_remote2local_dict())
	else:
		break


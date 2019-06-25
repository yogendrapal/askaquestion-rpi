import face_recognition
import cv2
from config import *
import json
import numpy as np


'''
This function will generate 2 face encodings for the person in
front of the camera and will return it. If no face is found for
100 frames, then None is returned.
'''
def generate_face_encodings(video_device=VIDEO_DEVICE):
	retry = 1
	while retry < 10:
		try:
			if retry == 10:
				return
			video_capture = cv2.VideoCapture(video_device)
		except:
			time.sleep(3)
			retry+=1

	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,160)
	video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,120)

	face_locations = []
	frame_count = 0
	skipframe = False
	target_skip_frame = 0

	face_encodings = []

	while True:
		# Grab a single frame of video
		ret, frame = video_capture.read()
		frame_count += 1
		if frame_count == target_skip_frame:
			skipframe = False

		rgb_frame = frame[:, :, ::-1]

		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_frame)

		if len(face_locations) == 1 and not skipframe:
			if len(face_encodings) < NUM_FACE_ENCODINGS_PER_RECORD:
				fenc = face_recognition.face_encodings(rgb_frame, face_locations)[0]
				face_encodings.append(fenc)
				target_skip_frame = frame_count + MIN_FRAME_SKIP_BW_TWO_ENCODINGS
				skipframe = True
			else:
				break

		if frame_count > MAX_FRAME_COUNT:
			return None
		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	print('frame-count:',frame_count)
	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()
	print('[INFO]: returning face encodings...\n')
	return face_encodings

'''
This function will store the passed fencs into the npz file with the name fid.
fencs contain the face encodings of the video with local id as fid
'''
def store_face_encodings(fencs, fid):
	try:
		npz = np.load(FACE_ENCS_NPZ_PATH)
		fe_data = dict(npz)
	except:
		fe_data = {}
	for i in range(len(fencs)):
		fe_data[fid+('_%d'%(i))] = fencs[i]
	np.savez(FACE_ENCS_NPZ_PATH,**fe_data)
	print('[INFO]: Saved face encodings...\n')


'''
This function gets all stored face encodings from the npz file and
creates a list of encodings and fids to be used for comparision
'''
def fetch_all_face_encodings():
	try:
		npz = np.load(FACE_ENCS_NPZ_PATH)
		fe_data = dict(npz)
	except:
		fe_data = {}
	fencs = []
	fenc_ids = []
	# print()
	# print(fe_data)
	# print()
	for fid in fe_data:
		fenc_ids.append(fid.split('_')[0])
		fencs.append(fe_data[fid])
	return fencs,fenc_ids
	print('[INFO]: fetched face encodings...\n')

'''
This function removes all the face encodings corresponding to the
passed fid. And updates the npz file.
'''
def remove_face_encodings(fid):
	try:
		npz = np.load(FACE_ENCS_NPZ_PATH)
		fe_data = dict(npz)
	except:
		return
	for i in range(NUM_FACE_ENCODINGS_PER_RECORD):
		enc = fe_data.pop(fid+('_%d'%i),None)
		if not enc:
			break
	np.savez(FACE_ENCS_NPZ_PATH,**fe_data)



'''
This function runs the face recogntion and tries to the match
the face in front of the camera with the stored face encodings.
if a match is found it returns the corresponding fids else it returns empty set
'''
def fetch_fid(video_device=VIDEO_DEVICE):
	retry = 1
	while retry < 10:
		try:
			video_capture = cv2.VideoCapture(video_device)
			print('Please look into the camera...')
			break
		except:
			time.sleep(2)
			retry+=1
	if(retry==10):
		return
	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,160)
	video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,120)
	known_fencs, known_fids = fetch_all_face_encodings()

	frame_count = 0

	while True:
		# Grab a single frame of video
		ret, frame = video_capture.read()
		frame_count += 1

		rgb_frame = frame[:, :, ::-1]

		face_locations = face_recognition.face_locations(rgb_frame)
		if len(face_locations) > 0:
			print('[INFO]: detected %d face(s).\n'%len(face_locations))
		face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

		res_fid = set()
		for enc in face_encodings:
			matches = face_recognition.compare_faces(known_fencs, enc,tolerance=FACE_DISTANCE_TOLERANCE)
			# print(matches)
			# face_distances = face_recognition.face_distance(known_fencs, enc)
			# print(face_distances)
			# best_match_index = np.argmin(face_distances)
			# if matches[best_match_index]:
			# 	name = known_fids[best_match_index]

			if True in matches:
				for m in range(len(matches)):
					if matches[m]:
						res_fid.add(known_fids[m])
				break
		if res_fid:
			break

		if frame_count > MAX_FRAME_COUNT:
			break

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	video_capture.release()
	cv2.destroyAllWindows()

	return res_fid
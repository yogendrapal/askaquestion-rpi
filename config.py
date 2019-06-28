#Config file for settings

try:
	from authinfo import *
except:
	print('[ERROR]: Device Initialization is incomplete. Please run init.py')
	MACHINE_ID = 'UNKNOWN'
	INSTITUTE_ID = 'UNKNOWN'

RPI = False

API_HOST = '10.196.11.165'
API_PORT = 8081
OUTPUT_DIR = 'output/'
ANSWER_DIR = 'answers/'
RECORD_VIDEO_ONLY = False
if RPI:
	RPI_CMD = True
	LOW_SETTING = False
else:
	RPI_CMD = False
	LOW_SETTING = True

VIDEO_DEVICE = 0


DB_PATH = 'database.sqlite3'
FACE_ENCS_NPZ_PATH = 'fenc.npz'

MAX_FRAME_COUNT = 100
NUM_FACE_ENCODINGS_PER_RECORD = 1
MIN_FRAME_SKIP_BW_TWO_ENCODINGS = 5
FACE_DISTANCE_TOLERANCE = 0.42	#reduce to get more strict matches, increase otherwise

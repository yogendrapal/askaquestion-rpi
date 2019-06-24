#Config file for settings

MACHINE_ID = 'XYZ'
API_HOST = '104.237.9.77'
API_PORT = 8081
OUTPUT_DIR = 'output/'
RECORD_VIDEO_ONLY = True
LOW_SETTING = False
VIDEO_DEVICE = 0

DB_PATH = 'database.sqlite3'
FACE_ENCS_NPZ_PATH = 'fenc.npz'

MAX_FRAME_COUNT = 100
NUM_FACE_ENCODINGS_PER_RECORD = 2
MIN_FRAME_SKIP_BW_TWO_ENCODINGS = 5
FACE_DISTANCE_TOLERANCE = 0.42	#reduce to get more strict matches, increase otherwise

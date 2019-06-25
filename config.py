#Config file for settings


MACHINE_ID = 'AbC'
API_HOST = '10.196.17.146'
API_PORT = 8081
OUTPUT_DIR = 'output/'
RECORD_VIDEO_ONLY = False
RPI_CMD = True
LOW_SETTING = False
VIDEO_DEVICE = 0

DB_PATH = 'database.sqlite3'
FACE_ENCS_NPZ_PATH = 'fenc.npz'

MAX_FRAME_COUNT = 100
NUM_FACE_ENCODINGS_PER_RECORD = 1
MIN_FRAME_SKIP_BW_TWO_ENCODINGS = 5
FACE_DISTANCE_TOLERANCE = 0.42	#reduce to get more strict matches, increase otherwise

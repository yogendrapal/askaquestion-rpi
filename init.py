import getpass
import shortuuid
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

API_HOST = '192.168.43.244'
API_PORT = 3000

while True:
	print('Enter the device id (leave blank to auto generate device id): ',end="")
	did = input()
	if did == "":
		did = str(shortuuid.uuid())
	print('Device ID will be set as %s'%(did))
	print('Enter E-Mail: ',end ="")
	email = input()
	pwd = getpass.getpass('Enter Password: ')

	post_data = {
		'email':email,
		'password':pwd,
		'deviceId':did
	}

	m = MultipartEncoder(fields = post_data)
	# post_data = json.dumps(post_data)
	# post_json = json.loads(post_data)

	#now try to connect with the app server
	API_ENDPOINT = "http://%s:%d/deviceReg" %(API_HOST,API_PORT)
	# headers = {'Accept' : 'application/json', 'Content-Type' : 'multipart/form-data'}

	try:
		# r = requests.post(API_ENDPOINT,data = post_data,headers={'Content-Type': 'multipart/form-data'})
		r = requests.post(API_ENDPOINT,data = m,headers={'Content-Type': m.content_type})#files=post_data, headers = headers)
	except:
		print('[ERROR]: Unable to communicate with the server! Please ensure that HOST & PORT are properly configured.\n')
		continue

	response_text = r.text
	print(response_text)
	response_json=json.loads(response_text)

	iid = None
	if 'Institute Id' in response_json:
		print('Authentication Successful\n')
		iid = response_json['Institute Id']
	else:
		print("BAD email or password!\n")
		continue

	f = open('authinfo.py','w')
	f.write('MACHINE_ID = "%s"\n'%(did))
	f.write('INSTITUTE_ID = "%s"\n'%(iid))
	f.close()
	break
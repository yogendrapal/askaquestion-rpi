import getpass
import shortuuid
import json

API_HOST = 'localhost'
API_PORT = 1111

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

	post_data = json.dumps(post_data)
	post_json = json.loads(post_data)

	#now try to connect with the app server
	API_ENDPOINT = "http://%s:%d/register" %(API_HOST,API_PORT)
	headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}

	try:
		r = requests.post(url = API_ENDPOINT, data=post_json,headers=headers)
	except:
		print('[ERROR]: Unable to communicate with the server! Please ensure that HOST & PORT are properly configured.\n')
		continue

	response_text = r.text
	response_json=json.loads(response_text)

	iid = None
	if 'insituteId' in response_json:
		print('Authentication Successful\n')
		iid = response_json['insituteId']
	else:
		print("BAD email or password!\n")

	f = open('authinfo.py','w')
	f.write('MACHINE_ID = "%s"\n'%(did))
	f.write('INSTITUTE_ID = "%s"\n'%(iid))
	f.close()
	break
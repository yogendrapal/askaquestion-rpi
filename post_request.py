
# importing the requests library 
import requests 
import json
import time

def postjson(jsonfile,vidname):
	# defining the api-endpoint  
	API_ENDPOINT = "http://localhost:8081/question/add"
	  
	
	  
	# sending post request and saving response as response object
	
	with open("output/"+jsonfile) as json_file:
		json_data = json.load(json_file) 
		json_data1=json.dumps(json_data)
	print(json_data1)
	headers = {'Authorization' : 'No Auth', 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	r = requests.post(url = API_ENDPOINT, data=json_data1,headers=headers)

	
	# extracting response text  
	response_text = r.text
	print("The pastebin URL is:%s"%response_text)
	make_json=json.loads(response_text)


	id=make_json["id"] 
	files = {'file': ('%s.mp4'%id,open("output/"+vidname, 'rb'),'video/mp4')}
	#headers = {'Content-type':'form-data'}
	#with requests.Session() as session:
		#del session.headers['User-Agent']
		#del session.headers['Accept-Encoding']
	time.sleep(1)
	response = requests.post("http://localhost:8081/question/add/%s"%id, files=files)
	
		
	print("\n\n",response.text)
	

   
   

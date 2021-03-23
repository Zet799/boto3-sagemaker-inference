import base64
import json
import numpy as np
import cv2
import boto3
from time import time

# run boto3 client sagemaker
ENDPOINT_NAME = ''#put sagemaker endpoint
runtime = boto3.client('runtime.sagemaker')

img_path = 'img.jpg'

with open(img_path, "rb") as img:
	img_b64 = base64.b64encode(img.read())

t_inicial1 = time()
img_d = base64.decodebytes(img_b64)
img_buffer = np.frombuffer(img_d, dtype=np.uint8)

img = cv2.imdecode(img_buffer, flags=cv2.IMREAD_COLOR)
img = img/255.0
arr = img.reshape((1,) + img.shape)

data = {
	'instances': arr.tolist()
}

tiempo_inicial = time()
try:
	response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
					Body=json.dumps(data),
					ContentType='application/json')

	tiempo_final = time()
	print(tiempo_inicial - t_inicial1)
	print(tiempo_final-tiempo_inicial)
	result = response['Body'].read().decode()
	print(result)
except Exception as e:
	print("Error in log")
	#print(e)
	file = open("error.log","w")
	file.write(str(e))
	file.close()




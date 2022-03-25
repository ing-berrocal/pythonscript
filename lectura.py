#!/usr/bin/python

import os
import re
import requests
import shutil
import threading

file_path = "C:\\Users\\DELL\\Downloads\\MORALES 279 - VIEJIO.csv"
file = open(file_path,'r')

result_path = 'D:\\Python\\result\\'

contador = 0

def buildThread(index,path,url):
	
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		contenido = response.headers['content-type']
		if re.match('image/*',contenido):
			with open(path+'\\'+str(index)+'.jpg', 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)	
	print('Finalizado url:',url,' ruta: ',path,' index:',index, ' status:',response.status_code)
	del response

while True:
	data = file.readline()
	if not data:
		break
	if contador == 0:
		contador = contador + 1
		continue		
	txt_split = data.split(';')

	directorio = txt_split[0]

	#for idx,item in list(enumerate(txt_split)):
	
	result_path_tmp = (result_path+directorio)
	if not os.path.exists(result_path_tmp):				
		os.makedirs(result_path_tmp)				
		print(result_path_tmp)		
	for item in range(1,len(txt_split)):
		if re.match('http(s+)://*',txt_split[item]):
			hilo = threading.Thread(target=buildThread, args=(item,result_path_tmp,txt_split[item]))
			hilo.start()
			hilo.join()
			#buildThread(item,result_path_tmp,txt_split[item])
			print(result_path_tmp,txt_split[item])		
	
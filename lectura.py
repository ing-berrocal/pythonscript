#!/usr/bin/python

import os
import re
import requests
import shutil
import threading
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

pattern = re.compile('https://[^,;]+')

params = sys.argv[1:]

#file_path = "C:\\Users\\DELL\\Downloads\\MORALES 279 - VIEJIO.csv"
#result_path = 'D:\\Python\\result\\'

directory = os.getcwd()

file_path = params[0]
result_path = params[1]

file = open(file_path,'r', encoding="utf8")

contador = 0	

def buildThread(index,path,url):
	if re.match('http(s+)://*',url):
		response = requests.get(url, stream=True)
		if response.status_code == 200:
			contenido = response.headers['content-type']
			if re.match('image/*',contenido):
				with open(path+'\\'+str(index)+'.jpg', 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)	
		print('Finalizado url:',url,' ruta: ',path,' index:',index, ' status:',response.status_code)					

while True:
	data = file.readline()
	if not data:
		break
	if contador == 0:
		contador = contador + 1
		continue		
	
	result = re.search(pattern,data)	
	if result:
		result = re.findall(pattern,data)
		
		txt_split = data.split(';')
		directorio = txt_split[0]
		
		#valida si es numero para creacion de directorio
		if re.match('\d',directorio):
			result_path_tmp = (result_path+directorio)
			if not os.path.exists(result_path_tmp):				
				os.makedirs(result_path_tmp)				
			num_elementos = len(result)
			#Generamos hilo para guardar las imagenes
			for idx in range(0,num_elementos):
				hilo = threading.Thread(target=buildThread, args=(idx,result_path_tmp,result[idx]))
				hilo.start()
			print('Se creo para ',directorio,num_elementos, 'elementos...')
			main_thread = threading.main_thread()
			for t in threading.enumerate():
				if t is main_thread:
					continue
				logging.debug('joining %s', t.getName())
				t.join()
	#for idx,item in list(enumerate(txt_split)):
	#if re.match('\D',directorio):
		#print('Linea : ',contador,'se omite item porque el primer item no es un numero',directorio)
		#continue
		
	#result_path_tmp = (result_path+directorio)
	#if not os.path.exists(result_path_tmp):				
	#	os.makedirs(result_path_tmp)				
	#	print(result_path_tmp)		
	#for item in range(1,len(txt_split)):		#if re.match('http(s+)://*',txt_split[item]):
	#	txt_urls = txt_split[item].split(',')
	#	for idxurl in range(0,len(txt_urls)):					
	#		hilo = threading.Thread(target=buildThread, args=(item,result_path_tmp,txt_urls[idxurl]))
	#		hilo.start()			
	#		#buildThread(item,result_path_tmp,txt_split[item])
	#		print(result_path_tmp,txt_split[item])		

#main_thread = threading.main_thread()
#for t in threading.enumerate():
#    if t is main_thread:
#        continue
#    logging.debug('joining %s', t.getName())
#    t.join()	

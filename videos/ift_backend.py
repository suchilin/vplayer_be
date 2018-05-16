#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DR(C) Klatus Software, 2017, ONRA 11/01/17
# DR(C) Klatus Software, 2017, ONRA 25/04/17
# Funciones de backend para analíticos de IFT

import ffmpy    # Wrapper de ffmpeg para python
import glob     # Para el listado de directorios y archivos
import requests # Para hacer las llamadas POST a la API de HPE
import json     # Para formatear las respuestas de la API de HPE
import time
import os
import shutil
import threading
#import queue
ip = 'http://ift.klatus.com/ift/ift/static/mpg/*.jpg'#esto es para personajes
# Ejmplos
text ='text=Acomp%C3%A1%C3%B1enos+en+el+AWS+Cloud+Experience+CDMX+y+conozca+c%C3%B3mo+la+plataforma+de+servicios+de+cloud+computing+de+Amazon+Web+Services+tiene+ayudado+clientes+y+qu%C3%A9+beneficios+ellos+han+logrado+para+su+negocio+tras+usar+AWS.'
textFile = 'noticiero.txt'#Speech to text
#foto = 'http://mxcdn02.mundotkm.com/2017/04/amlo-6-600x300.jpg'
foto = 'https://dl.dropboxusercontent.com/u/23422932/andres.jpg'#Envio fotos
foto_xxx = 'https://dl.dropboxusercontent.com/u/23422932/example_xxx.png'

hot_1 = 'https://dl.dropboxusercontent.com/u/23422932/hot_1.png'
hot_2 = 'https://dl.dropboxusercontent.com/u/23422932/hot_2.png'
hot_3 = 'https://dl.dropboxusercontent.com/u/23422932/hot_3_blur.png/'
hot_4 = 'https://dl.dropboxusercontent.com/u/23422932/hot_4.png'
hot_5 = 'https://dl.dropboxusercontent.com/u/23422932/hot_5.png'

# HPE apikey
hpekey = 'c0ea2231-ab38-446c-9e8d-0194d3d6f51e'
# MCS apikey
mcs_emotions_key = 'c1728b4a0bcf45038a31d802c50aab14'
mcs_faces_key = '31c0c13a9abc421184121b4b78405b3d'
mcs_vision_key = 'eeaa166d5ebf4d32b8fed3a1b34e37ce'#Personajes
# PATHS
BASE_PATH = os.getcwd()
pathLogos = os.path.join(BASE_PATH,'static/mpg/')
pathPersonas= os.path.join(BASE_PATH, 'static/mpg_personas/')
pathResult_Personas = os.path.join(BASE_PATH, 'static/mpgresult_personas/')
pathResult = os.path.join(BASE_PATH, 'static/mpgresult/')
pathVideos = os.path.join(BASE_PATH,'static/video/')
pathAudios = os.path.join(BASE_PATH,'static/audio/')
pathStatic = os.path.join(BASE_PATH, 'static/mpgresult/')
pathStatic_Personas= os.path.join(BASE_PATH, 'static/mpgresult_personas/')

# Archivo de ejemplo, desde web se debe hacer upload o hacer referencia a una URL que lo contenga
#fin = 'samples/Canal_2_04-10-2016_22-03-41_19216810146_Streaming_2_18249_H264_PROXY.mp4'
#fin2 = 'samples/sinvideo.mp4'
#fin3 = 'samples/1034392-MI_ABIERTA_CANAL2_04012017_214159_DF_31852.mp4'
#fin4 = 'samples/coca.mp4'
#fin5 = 'samples/city.mp4'
#fin6 = 'samples/pena.mp4'

# Ejemplo en consola: ffmpeg -i Canal_2_04-10-2016_22-03-41_19216810146_Streaming_2_18249_H264_PROXY.mp4 -vf fps=1 -qscale:v 2 outputHD/output_%05d.jpg
def ff_mp4_2_jpg(intervalo_de_muestra, video):
    # Directorio y formato en el que se depositarán las imagenes JPG
    #lista=[]
    print (video)
    fsout = pathLogos + 'output_%05d.jpg' #'''/home/duraznito/app3/ift/helloweb/hello/static/mpg/output_%05d.jpg'''

    """Extrae de un archivo MP4 de video, imágenes JPG usando la variable 'intervalo_de_muestra'"""
    ff = ffmpy.FFmpeg(
        inputs = { video: None},
        outputs = { fsout: '-vf fps=' + str(intervalo_de_muestra) +' -qscale:v 2 '}
    )
    res = ff.run()
    directorios = glob.glob(pathLogos + '*.jpg')
    #for d in directorios:
        #lista.append("http://"+d[5:])#ruta de la foto


    return 0

def ff_mp4_2_jpg_Personas(intervalo_de_muestra, video):
    # Directorio y formato en el que se depositarán las imagenes JPG
    lista=[]
    print (video)
    fsout = pathPersonas + 'output_%05d.jpg' #'''/home/duraznito/app3/ift/helloweb/hello/static/mpg/output_%05d.jpg'''
    print (fsout)

    """Extrae de un archivo MP4 de video, imágenes JPG usando la variable 'intervalo_de_muestra'"""
    ff = ffmpy.FFmpeg(
        inputs = { video: None},
        outputs = { fsout: '-vf fps=' + str(intervalo_de_muestra) +' -qscale:v 2 '}
    )
    res = ff.run()
    directorios = glob.glob(pathPersonas + '*.jpg')
    for d in directorios:
        lista.append("http://"+d[5:])#ruta de la foto


    return lista

# Ejemplo en consola: curl -X POST --form \"file=@output_00002.jpg\" --form \"image_type=simple\" --form \"indexes=corporatelogos\" --form \"hpekey=c0ea2231-ab38-446c-9e8d-0194d3d6f51e\" https://api.havenondemand.com/1/api/sync/recognizeimages/v1
def hpe_image_recognition(key, path, st):
    """Envía a HPE iterativamente cada cuadro del video para identificaciín de logos"""
    url = 'https://api.havenondemand.com/1/api/sync/recognizeimages/v1'
    files = glob.glob(path + '*.jpg')
    logos = dict() #[] #
    for f in files:
        files = {'file': open(f,'rb')}
        data = {
            'image_type' : 'complex_3d', # [simple, complex_2d, complex_3d]
            'indexes' : 'corporatelogos',
            'apikey' : hpekey
        }
        req = requests.post(url, files = files, data = data)
        print (f + ':' + str(req.status_code) + ':' + str(req.json()))
        result = req.json()
        print (result)
        if len (result["object"] ) > 0 :
            imgPath = pathResult  + st + '/' + str (os.path.basename(f))
            logos[pathStatic + st + '/' + str (os.path.basename(f))] = result["object"][0]["name"]#            logos.append(result["object"][0]["name"])#
            print (f)
            print (st+"------------------------------")
            shutil.copyfile(f, imgPath) #copia la imagen a otra rura
    print(len(files))
    return logos

# Nuevo
def mcs_vision_people(key, imageFile,st):#Personajes-----------------------------------
    url_mcs = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze'
    personalidades=dict()
    json_resp=''
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key' : key,
    }
    json_env = {
        'url' : imageFile,
    }
    params = {
        #'visualFeatures' : 'Adult, Description, Faces',
        'visualFeatures' : 'Adult, Description',
        'details' : 'Celebrities',
        'language' : 'en',
    }
    with open(imageFile, 'rb') as f:
        img_data = f.read()
    data = img_data
    req = requests.request('POST', url_mcs, json = json_env, data = data, headers = headers, params = params )
    #print ('Response CODE: ' + str(req.status_code))
    resultado = req.json()
    print (req.json())
    if resultado["adult"]["isAdultContent"] == 'True' or resultado["adult"]["isRacyContent"]:
        f= imageFile
        imgPath = pathResult_Personas + st + '/' + str (os.path.basename(f))
        shutil.copyfile(f, imgPath)
        d = resultado["description"]["captions"][0]["text"]
        aSc = round((resultado["adult"]["adultScore"]) * 100, 2)
        raSc = round(resultado["adult"]["racyScore"] * 100 , 2)
        imgstat= pathStatic_Personas + st + '/' +str (os.path.basename(f))
        datos = ({'ruta':imgstat,'description':d,'adultScore':aSc,'racyScore':raSc})
        json_make = json.dumps(datos)
        json_resp= json.loads(json_make)
    try:
        categorias = resultado["categories"][0]
        #elif "detail" in resultado["categories"][0]:
        if "detail" in resultado["categories"][0]:
            if len(resultado["categories"][0]["detail"]["celebrities"]) > 0:
                f= imageFile
                imgPath = pathResult_Personas + st + '/' + str (os.path.basename(f))
                shutil.copyfile(f, imgPath)
                nombreartista= resultado["categories"][0]["detail"]["celebrities"][0]["name"]
                imgstat= pathStatic_Personas + st + '/' +str (os.path.basename(f))
                json_make = json.dumps({'ruta':imgstat,'celebridad':nombreartista})
                json_resp= json.loads(json_make)
    except KeyError:
        pass

    return json_resp

#--------------------------------------------------------------------------
# Ejemplo en consola: ffmpeg -i Canal_2_04-10-2016_22-03-41_19216810146_Streaming_2_18249_H264_PROXY.mp4 -codec copy -vn sinvideo.mp4
def ff_mp4_2_mp4_sinvideo(video):
    """Le quita la imágen al video MP4 para transmitir a HPE sólo el audio para la transcripción"""
    fsout = pathAudios + 'audio.mp4'
    ff = ffmpy.FFmpeg(
        inputs = { video: None},
        outputs = { fsout: '-codec copy -vn'}
    )
    res = ff.run()
    return res

def hpe_speech_2_text(key, videofile):
    """Envía un archivo MP4 de video a los servicios HPE para obtener su trascripción"""
    url = 'https://api.havenondemand.com/1/api/async/recognizespeech/v1'
    print ('videofile :' + str (videofile))
    files = {'file': open(videofile,'rb')}
    data = {
        'language' : 'es-LA',
        #'interval' : '10000',
        'apikey' : hpekey
    }
    req = requests.post(url, files = files, data = data, )
    print ('Response CODE: ' + str(req.status_code))
    print (json.dumps(req.json(), indent = 2, sort_keys = True))
    result = req.json()
    #print (result)
    jobID = result["jobID"]
    #print (jobID)
    return jobID

#Nuevo
def hpe_sentimental(key, text):#Texto de speech to text sentimientos
    url = 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v2'
    #files = {'file': open(textFile,'r')}
    data = {
        'language' : 'spa',
        'text' : text,
        'mode' : 'precision',
        'apikey' : key
    }
    req = requests.post(url,data = data)
    print ('Response CODE: ' + str(req.status_code))
    print (json.dumps(req.json(), indent = 2, sort_keys = True))
    result = req.json()
    #print (result)
    promedio = result["sentiment_analysis"][0]["aggregate"]
    # positive = result["sentiment_analysis"][0]["positive"]
    # negative = result["sentiment_analysis"][0]["negative"]
    print(promedio)
    # print(positive)
    # print(negative)
    return result

#Nuevo
def mcs_emotion_recognition(key, imageFile):
    url_mcs = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key' : key,
    }
    json = {
        'url' : imageFile,
    }
    params = None
    data = None
    req = requests.request('POST', url_mcs, json = json, data = data, headers = headers, params = params )
    print ('Response CODE: ' + str(req.status_code))
    #print (json.dumps(req.json(), indent = 4, sort_keys = True))
    print(req.json())
    return 0

def hpe_status_job(key, jobid):
    """Permite consultar el estatus de una petición en HPE"""
    url = 'https://api.havenondemand.com/1/job/status/' + jobid
    data = {
        'apikey' : hpekey
    }
    req = requests.post(url, data = data)
    print ('Response CODE: ' + str(req.status_code))
    print (json.dumps(req.json(), indent = 2, sort_keys = True))
    result = req.json()
    #status = result["status"]
    #print (status)
    return result

def hpe_recover_result(key, jobid):
    """Recupera la transcripción en JSON devuelta por HPE"""
    url = 'https://api.havenondemand.com/1/job/result/' + jobid
    data = {
        'apikey' : hpekey
    }
    req = requests.post(url, data = data)
    print ('Response CODE: ' + str(req.status_code))
    print (json.dumps(req.json(), indent = 2, sort_keys = True))
    result = req.json()
    #print (result)
    content = result["actions"][0]["result"]["document"][0]["content"]
    return content

def decodeTexto (video, st, que):#, q):
    #audio = ff_mp4_2_mp4_sinvideo(pathVideos + str (video))
    #print (audio) ,
    jobID = hpe_speech_2_text(hpekey, str (video))
    content = "error"
    while (True): # mientras este con estatus 'queued' seguira intentando cada 30 segundos
        time.sleep(30)
        result = hpe_status_job(hpekey, jobID)
        print (result)
        status = result["status"]
        print (status)
        if status=="finished" :
            print ("Finalizado")
            content = result["actions"][0]["result"]["document"][0]["content"]
            #content = hpe_recover_result(hpekey, 'w-eu_472b5986-1b3d-4f1e-a179-c90245f1c85c') no es necesario llamar servicio
            que.put(content)
            return content
        elif status == "failed":
            print ("Fallo")
            #q.put(content)
            return content

def decodeLogos (video, st, que):#, q):
    ff_mp4_2_jpg(1, str (video))
    logos = hpe_image_recognition(hpekey, pathLogos, st)
    delPathTemp()
    print (logos)
    que.put(logos)
    return (logos)


def decodeSentimientos(video,st,que):
        jobID = hpe_speech_2_text(hpekey, str(video))
        content = "error"
        while (True): # mientras este con estatus 'queued' seguira intentando cada 30 segundos
            time.sleep(5)
            result = hpe_status_job(hpekey, jobID)
            print (result)
            status = result["status"]
            print (status)
            if status=="finished" :
                print ("Finalizado")
                content = result["actions"][0]["result"]["document"][0]["content"]

                #content = hpe_recover_result(hpekey, 'w-eu_472b5986-1b3d-4f1e-a179-c90245f1c85c') no es necesario llamar servicio
                break
        #print(content)
        json = hpe_sentimental(hpekey,content)
        print(json)
        que.put(json)
        return json

def decodePersonajes(video,st,que):
    print('hello from decode personajes')
    ruta=[]
    ff_mp4_2_jpg_Personas(1, str(video))
    ruta = glob.glob(pathPersonas+"*.jpg")
    personaje=[]
    t=0
    os.mkdir(pathResult_Personas + st)
    k=0
    for r in ruta:
        print (str(k)+".-"+r)
        k+=1
        t=t+1
        time.sleep(2)
        eljson = mcs_vision_people(mcs_vision_key, r,st);
        if eljson != '':
            personaje.append(mcs_vision_people(mcs_vision_key, r,st))
        if t == 10:
            time.sleep(1)

    delPathTemp_Personas()
    que.put(personaje)
    print (personaje)
    return personaje

def delPathTemp ():
    shutil.rmtree(pathLogos)
    os.mkdir(pathLogos)

def delPathTemp_Personas():
    shutil.rmtree(pathPersonas)
    os.mkdir(pathPersonas)

def main():
    #hpe_sentimental(hpekey, text)
    mcs_vision_people(mcs_vision_key, hot_1)
    #mcs_emotion_recognition(mcs_emotions_key, foto)
 #   decodeLogos(hpekey, fin4)
    # Para identificación de logos
    #ff_mp4_2_jpg(1, fin4)
    #hpe_image_recognition(hpekey, '/home/duraznito/Escritorio/IFT/IFT/output/*.jpg')

    # Para speech to text de un archivo de video
    #hpe_speech_2_text(hpekey, fin6)
    #hpe_status_job(hpekey, 'w-eu_e9d01896-ce58-4488-a843-a25f6078157d')
    #hpe_recover_result(hpekey, 'w-eu_fd04e285-d41c-4789-b2cf-2ddc01e0ccfe')


  #  print ("BEGIN")
    #content = decodeText(hpekey, fin6)
    #print (content)
   # print ("END")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from videos.serializers import VideoSerializer, CatalogacionSerializer
from rest_framework import generics
from .models import Video, Catalogacion
import django_filters
import ffmpy
import os
import sys
import json
import time
import datetime
import threading
from multiprocessing import Queue
from videos import ift_backend

pathResult = 'static/mpgresult/'
texto = ''
logos = dict()
emociones = ''

def cortarVideo(vFilepath, start, end):
    inicio = str(datetime.timedelta(seconds=start))
    tiempo= str(datetime.timedelta(seconds=end-start))
    output = 'static/clips/'+vFilepath.replace('static/','').replace('.mp4','')+'__'+str(start).replace('.','')+str(end).replace('.','')+'.mp4'
    if os.path.isfile(output):
        return output
    else:
        outputs = '-ss %s -t %s -async 1'%(inicio, tiempo)
        ff = ffmpy.FFmpeg(
            inputs={vFilepath:None},
            outputs={output:outputs}
        )
        ff.run()
    return output

def display_video(request, video, options, prueba):
    file = 'static/video/' + str(video)
    texto = ''
    logos = ''
    emociones = ''
    imagenes=''
    personas=''
    os.mkdir(pathResult  + prueba)
    showtexto='none'
    showlogos='none'
    showEmociones='none'
    threads = [None,None,None,None]
    qT = Queue()
    qL = Queue()
    qE = Queue()
    qP = Queue()

    for o in options:
        if o == 'TEX':
            threads[0] = threading.Thread(target=ift_backend.decodeTexto, args=(video, prueba, qT))
            threads[0].start()
            showtexto='block'
        elif o== 'LOG':
            threads[1] = threading.Thread(target=ift_backend.decodeLogos, args=(video, prueba, qL))
            threads[1].start()
            showlogos='block'
            print (imagenes)
        elif o=='EMO':
            threads[2] = threading.Thread(target=ift_backend.decodeSentimientos, args=(video,prueba,qE))
            threads[2].start()
            showEmociones='block'
        elif o == 'PER':
            threads[3] = threading.Thread(target=ift_backend.decodePersonajes, args=(video,prueba,qP))
            threads[3].start()


    num=0
    segundo=[]
    segundocelb=[]
    minutocelb=[]
    segundoadu=[]
    minutoadu=[]
    minuto=[]
    num1=0
    tag_list_positivo=[]
    tag_list_negativo=[]
    path_imagenes=[]
    positivo_porcentaje=0
    negativo_porcentaje=0
    resumen_porcentaje=0
    resumen_sentimiento=''
    personajes=[]
    nombreceleb=[]
    rutaceleb=[]
    ruta=[]
    adultScore=[]
    racyScore=[]
    description=[]
    for o in options:
        if o == 'TEX':
            threads[0].join()
            texto = qT.get()
        elif o=='LOG':
            threads[1].join()
            logos = qL.get()
           
            for t in logos:
                print(t)
                tiempo=int(t[41:-4])
                if tiempo > 60:
                    minutos=tiempo/60
                    segundos=tiempo%60
                    minuto.append(minutos)
                    segundo.append(segundos)
                  
                else:
                    segundo.append(tiempo)
                   
           
        elif o=='EMO':
            threads[2].join()
            emociones = qE.get()
            resumen_porcentaje= emociones["sentiment_analysis"][0]["aggregate"]["score"]
            resumen_porcentaje= round(resumen_porcentaje * 100, 2)
            resumen_sentimiento=emociones["sentiment_analysis"][0]["aggregate"]["sentiment"]
            for i in emociones["sentiment_analysis"][0]["positive"]: 
                 #positivo= emociones["sentiment_analysis"][0]["positive"][0]["sentiment"]
                 tag_list_positivo.append(i["sentiment"])
                 #positivopor= emociones["sentiment_analysis"][0]["positive"][0]["score"]
                 n2=i["score"]
                 positivo_porcentaje=positivo_porcentaje+n2

                 num=num+1
                 #positivopor= round(positivopor * 100, 2)
            if num == 0:
                positivo_porcentaje=0;
            else:
                positivo_porcentaje=round((positivo_porcentaje/num) * 100,2)
            for i in emociones["sentiment_analysis"][0]["negative"]: 
                     #positivo= emociones["sentiment_analysis"][0]["positive"][0]["sentiment"]
                     tag_list_negativo.append(i["sentiment"])
                     #positivopor= emociones["sentiment_analysis"][0]["positive"][0]["score"]
                     n=i["score"]
                     negativo_porcentaje=negativo_porcentaje+n
                    
                     num1=num1+1
                     #positivopor= round(positivopor * 100, 2)
            if num1 == 0:
                negativo_porcentaje=0
            else:
                negativo_porcentaje=round((negativo_porcentaje/num1)*100,2)


        elif o== 'PER':
            threads[3].join()
            personajes= qP.get()
            #print(personajes)
            for p in personajes:
                
                #p = json.loads(p)

                ruta.append(str(p["ruta"]))
                racyScore.append(p["racyScore"])
                adultScore.append(p["adultScore"])
                description.append(str(p["description"]))
                

        nombres=[]    
        for l in logos:
            nombres.append(logos[l])

    return {
                'playing': file, 
                'texto': texto,
                'resumen_porcentaje':resumen_porcentaje,
                'resumen_sentimiento': resumen_sentimiento,
                'imagenes':logos,
                'showtexto':showtexto,
                'showlogos':showlogos,
                'showEmociones':showEmociones,
                'tag_list_positivo':tag_list_positivo,
                'positivo_porcentaje':positivo_porcentaje,
                'tag_list_negativo':tag_list_negativo,
                'negativo_porcentaje':negativo_porcentaje,
                'options':options,
                'segundos':segundo,
                'nombres':nombres,
                'nombreceleb':nombreceleb,
                'rutaceleb':rutaceleb,
                'ruta':ruta,
                'racyScore':racyScore,
                'adultScore':adultScore,
                'descripcion':description,
                'segundosceleb':segundocelb,
                'segundosadu':segundoadu
        }

class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('canal', 'fecha','hora')
    
class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'pk'
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    
class CatalogacionList(generics.ListCreateAPIView):
    queryset = Catalogacion.objects.all()
    serializer_class = CatalogacionSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('video',)
    
class CatalogacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = CatalogacionSerializer
    lookup_field = 'pk'
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    
class Testigo(APIView):
   def get(self, request, format=None):
        video_id = int(request.GET.get('video_id'))
        inicio = float(request.GET.get('inicio'))
        fin = float(request.GET.get('fin'))
        video = Video.objects.get(id=video_id)
        videoPath='static/'+video.path
        output = cortarVideo(videoPath, inicio, fin)
        return Response(output)
    
class Analiticos(APIView):
    def get(self, request, format=None):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')    
        video_id = int(request.GET.get('video_id'))
        inicio = float(request.GET.get('inicio'))
        fin = float(request.GET.get('fin'))
        options = request.GET.getlist('options')
        video = Video.objects.get(id=video_id)
        videoPath='static/'+video.path
        output = cortarVideo(videoPath, inicio, fin)
        result_ = display_video(request, output, options, str(st))
        return Response(result_)
        
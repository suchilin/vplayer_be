# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink

# Create your models here.
class Video(models.Model):
    canal = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.CharField(max_length=20)
    path = models.CharField(max_length=100)
    
    @permalink
    def get_absolute_url(self):
        return ('video-detail',(),{
                'id':self.pk
            })
    
class Catalogacion(models.Model):
    video = models.ForeignKey(Video)
    descripcion = models.TextField()
    genero = models.CharField(max_length=50)
    inicio = models.FloatField()
    fin = models.FloatField()

    @permalink
    def get_absolute_url(self):
        return ('catalogacion-detail',(),{
                'id':self.pk
            })
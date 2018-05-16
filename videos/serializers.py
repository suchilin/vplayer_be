from rest_framework import serializers
from .models import Video, Catalogacion

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        
class CatalogacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogacion
        fields = '__all__'
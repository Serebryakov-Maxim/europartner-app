from rest_framework import serializers
from .models import Pressform

class PressformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pressform
        fields = ['id','name', 'assembly', 'article', 'date_start', 'date_finish', 'priority', 'shield', 'type', 'status', 'year', 'date_modified']

class PressformLastModifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pressform
        fields = ['id','name', 'date_modified']
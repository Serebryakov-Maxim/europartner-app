from rest_framework import serializers
from .models import mw_Detail

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = mw_Detail
        fields = ['id','name', 'assembly', 'article', 'full_name', 'partner', 'quantity', 'date_start', 'date_finish', 'priority', 'shield', 'type', 'status', 'year', 'date_modified']

class DetailLastModifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = mw_Detail
        fields = ['id','name', 'date_modified']
from rest_framework import serializers
from .models import Partner

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name','full_name','code_1C','uuid_1C']
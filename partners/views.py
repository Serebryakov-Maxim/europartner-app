from django.shortcuts import render
from rest_framework.response import Response
from .serializers import PartnerSerializer
from .models import Partner
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class PartnerApiView(APIView):

    def get_object(self, id):
        '''Метод возвращает задание по id'''
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            return None
        
    def get_object_by_uuid(self, uuid_1C):
        '''Метод возвращает задание по uuid'''
        try:
            return Partner.objects.get(uuid_1C=uuid_1C)
        except Partner.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        '''Метод возвращает партнера по id'''
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        '''Создание/обновление партнеров'''
        data = {
            'uuid_1C': request.data.get('uuid_1C'), 
            'code_1C': request.data.get('code_1C'), 
            'name': request.data.get('name'),
            'full_name': request.data.get('full_name')
        }
        
        partner_instance = self.get_object_by_uuid(data['uuid_1C'])
        if not partner_instance:
            serializer = PartnerSerializer(data=data)
        else:
            serializer = PartnerSerializer(instance = partner_instance, data=data, partial = True)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
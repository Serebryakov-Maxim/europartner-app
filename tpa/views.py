from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Machine
from .serializers import MachineSerializer

def list(request):
    return render(request, 'tpa/list.html')


class MachineListApiView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):

        '''
        List all the todo items for given requested user
        '''
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
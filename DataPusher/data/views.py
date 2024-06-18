from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
# import request

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['GET'])
def get_destinations(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        destinations = account.destinations.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    destinations = account.destinations.all()
    
    for destination in destinations:
        headers = destination.headers
        url = destination.url
        method = destination.http_method.upper()
        
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method in ['POST', 'PUT']:
            response = requests.request(method, url, headers=headers, json=data)
        else:
            return Response({"error": "Invalid HTTP Method"}, status=status.HTTP_400_BAD_REQUEST)
        
        if response.status_code != 200:
            return Response({"error": "Failed to send data"}, status=response.status_code)
    
    return Response({"status": "success"}, status=status.HTTP_200_OK)


from http.client import ResponseNotReady
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from transaction.models import Transaction
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TCIBViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def payment(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            return Response("{}", status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def payment_return(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            return Response("{}", status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def status(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            return Response("{}", status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
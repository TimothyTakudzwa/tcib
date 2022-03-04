from django.shortcuts import render
from rest_framework import viewsets

from transaction.models import Transaction
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TCIBViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer
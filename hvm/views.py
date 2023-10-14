from django.shortcuts import render

# Create your views here.
from .models import LeadVisitor, Accompanying

from rest_framework import viewsets
from .serializers import LeadVisitorSerializer, AccompanyingSerializer

class LeadVisitorViewSet(viewsets.ModelViewSet):
    queryset = LeadVisitor.objects.all()
    serializer_class = LeadVisitorSerializer
    
class AccompanyingViewSet(viewsets.ModelViewSet):
    queryset = Accompanying.objects.all()
    serializer_class = AccompanyingSerializer


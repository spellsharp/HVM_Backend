from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.response import Response

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

@csrf_exempt
def getAccompanyingVisitors(request):
    if request.method == 'GET':
        lead_id = request.GET.get('lead_id', '')
        unique_id = request.GET.get('unique_id', '')

        if lead_id:
            lead_visitor = LeadVisitor.objects.filter(id=lead_id).first()

            if lead_visitor:
                accompanying_visitors = Accompanying.objects.filter(lead_visitor=lead_visitor)
                serializer = AccompanyingSerializer(accompanying_visitors, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({'message': 'Lead Visitor not found'})

        elif unique_id:
            accompanying_visitors = Accompanying.objects.filter(unique_id=unique_id)
            serializer = AccompanyingSerializer(accompanying_visitors, many=True)
            return JsonResponse(serializer.data, safe=False)
        
        else:
            return JsonResponse({'message': 'Accompanying Visitor not found'})

    return JsonResponse({'message': 'Visitor not found'})
            
        
        

@csrf_exempt
def getLeadVisitors(request):
    if request.method == 'GET':
        unique_id = request.GET.get('unique_id', '')
        lead_id = request.GET.get('lead_id', '')        
        if unique_id:
            lead_visitors = LeadVisitor.objects.filter(unique_id=unique_id)
        elif lead_id:
            lead_visitors = LeadVisitor.objects.filter(id=lead_id)
        else:
            lead_visitors = LeadVisitor.objects.all()
        serializer = LeadVisitorSerializer(lead_visitors, many=True)
        return JsonResponse(serializer.data, safe=False)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    
@csrf_exempt
def getAccompanyingVisitors(request):
    if request.method == 'GET':
        lead_unique_id = request.GET.get('lead_visitor_id', '')
        unique_id = request.GET.get('unique_id', '')
        lead_visitor = LeadVisitor.objects.filter(unique_id=lead_unique_id).values_list('id', flat=True).first()
        if lead_visitor:
            lead_visitor_id = lead_visitor.unique_id
        else:
            JsonResponse({'message': 'Lead Visitor not found'})  
        accompanying_visitors = Accompanying.objects.filter(lead_visitor=int(lead_visitor_id))
        if unique_id:
            accompanying_visitors = Accompanying.objects.filter(unique_id=unique_id)
        else:
            JsonResponse({'message': 'Accompanying Visitor not found'})
            
        serializer = AccompanyingSerializer(accompanying_visitors, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getLeadVisitors(request):
    if request.method == 'GET':
        unique_id = request.GET.get('unique_id', '')
        if unique_id:
            lead_visitors = LeadVisitor.objects.filter(unique_id=unique_id)
        else:
            JsonResponse({'message': 'Lead Visitor not found'})
        lead_visitors = LeadVisitor.objects.all()
        serializer = LeadVisitorSerializer(lead_visitors, many=True)
        return JsonResponse(serializer.data, safe=False)
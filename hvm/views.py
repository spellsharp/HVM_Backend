from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LeadVisitor, Accompanying
import datetime
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
        from_date, to_date = request.GET.get('from_date', ''), request.GET.get('to_date', '')  
        date = request.GET.get('date', '')
        if unique_id:
            lead_visitors = LeadVisitor.objects.filter(unique_id=unique_id)
        elif lead_id:
            lead_visitors = LeadVisitor.objects.filter(id=lead_id)
        elif date:
            lead_visitors = LeadVisitor.objects.filter(visiting_date=date)
        elif from_date and to_date:
            lead_visitors = LeadVisitor.objects.filter(visiting_date__range=[from_date, to_date])
        else:
            lead_visitors = LeadVisitor.objects.all()
        serializer = LeadVisitorSerializer(lead_visitors, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def is_expired(request):
    if request.method == 'GET':
        unique_id = request.GET.get('unique_id', '')
        lead_visitor = LeadVisitor.objects.filter(unique_id=unique_id).first()
        if lead_visitor:
            print(lead_visitor.valid_till) #2023-10-14 23:37:15.561043+00:00
            print(datetime.datetime.now()) #2023-10-14 17:38:35.502231
            if lead_visitor.valid_till.replace(tzinfo=None) < datetime.datetime.now():
                return JsonResponse({'message': 'expired'})
            else:
                return JsonResponse({'message': 'not expired'})
        else:
            return JsonResponse({'message': 'not found'})
    return JsonResponse({'message': 'Invalid Request Received (Not GET)'})
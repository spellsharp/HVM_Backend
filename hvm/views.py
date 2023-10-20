from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LeadVisitor, Accompanying, Receiver
import datetime
from rest_framework import viewsets, status, generics
from .serializers import LeadVisitorSerializer, AccompanyingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ReceiverSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer


class ReceiverViewSet(viewsets.ModelViewSet):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer
    # permission_classes = [IsAuthenticated]
    
    @csrf_exempt    
    def list(self, request):
        if request.method == 'GET':
            username = request.GET.get('username', '')
            if username:
                receivers = Receiver.objects.filter(username=username)
                serializer = ReceiverSerializer(receivers, many=True)
                return JsonResponse(serializer.data, safe=False)
            
            elif username == '':
                receivers = Receiver.objects.all()
                serializer = ReceiverSerializer(receivers, many=True)
                return JsonResponse(serializer.data, safe=False)
            
            else:
                return JsonResponse({'message': 'Receiver not found'})

class LeadVisitorViewSet(viewsets.ModelViewSet):
    queryset = LeadVisitor.objects.all()
    serializer_class = LeadVisitorSerializer
    # permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def list(self, request):
        if request.method == 'GET':
            unique_id = request.GET.get('unique_id', '')
            from_date, to_date = request.GET.get('from_date', ''), request.GET.get('to_date', '')  
            date = request.GET.get('date', '')
            
            if unique_id:
                lead_visitors = LeadVisitor.objects.filter(unique_id=unique_id)
            elif date:
                lead_visitors = LeadVisitor.objects.filter(visiting_date=date)
            elif from_date and to_date:
                lead_visitors = LeadVisitor.objects.filter(visiting_date__range=[from_date, to_date])
            else:
                lead_visitors = LeadVisitor.objects.all()
            serializer = LeadVisitorSerializer(lead_visitors, many=True)
            return JsonResponse(serializer.data, safe=False)
class AccompanyingViewSet(viewsets.ModelViewSet):
    queryset = Accompanying.objects.all()
    serializer_class = AccompanyingSerializer
    # permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def list(self, request):
        if request.method == 'GET':
            unique_id = request.GET.get('unique_id', '')
            lead_visitor_id = request.GET.get('lead_visitor_id', '')
            if unique_id:
                accompanying_visitors = Accompanying.objects.filter(unique_id=unique_id)
                serializer = AccompanyingSerializer(accompanying_visitors, many=True)
                return JsonResponse(serializer.data, safe=False)
            elif lead_visitor_id:
                lead_visitor = LeadVisitor.objects.filter(unique_id=lead_visitor_id).first()
                accompanying_visitors = Accompanying.objects.filter(lead_visitor=lead_visitor)
                serializer = AccompanyingSerializer(accompanying_visitors, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                accompanying_visitors = Accompanying.objects.all()
                serializer = AccompanyingSerializer(accompanying_visitors, many=True)
                return JsonResponse(serializer.data, safe=False)

    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(dict(request.data))
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ExpiryView(APIView):
    # permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            unique_id = request.GET.get('unique_id', '')
            if unique_id == '':
                return JsonResponse({'message': 'unique_id not provided'})
            lead_visitor = LeadVisitor.objects.filter(unique_id=unique_id).first()
            if lead_visitor:
                if lead_visitor.valid_till.replace(tzinfo=None) < datetime.datetime.now():
                    print(f"Expired: ID {unique_id}")
                    return JsonResponse({'message': 'expired', 'expired_datetime': lead_visitor.valid_till, 'expired_time': lead_visitor.valid_till.time(), 'expired_date': lead_visitor.valid_till.date()})
                else:
                    print(f"Not Expired: ID {unique_id}")
                    return JsonResponse({'message': 'not expired', 'expiry_datetime': lead_visitor.valid_till, 'expiry_time': lead_visitor.valid_till.time(), 'expiry_date': lead_visitor.valid_till.date()})
            else:
                return JsonResponse({'message': 'not found'})
        else:
            return JsonResponse({'message': f'{request.method} not allowed. Only GET allowed'})

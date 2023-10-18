from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LeadVisitor, Accompanying
import datetime
from rest_framework import viewsets, status, generics
from .serializers import LeadVisitorSerializer, AccompanyingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LeadVisitorViewSet(viewsets.ModelViewSet):
    queryset = LeadVisitor.objects.all()
    serializer_class = LeadVisitorSerializer
    permission_classes = [IsAuthenticated]
class AccompanyingViewSet(viewsets.ModelViewSet):
    queryset = Accompanying.objects.all()
    serializer_class = AccompanyingSerializer
    permission_classes = [IsAuthenticated]
    

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
        
# @csrf_exempt
# def create_lead_visitor(request):
#     if request.method == 'POST':
#         logged_in_user = request.user
#         lead_visitor = LeadVisitor(
#             full_name=request.data['full_name'], 
#             company_name=request.data['company_name'],
#             address=request.data['address'],
#             contact_number=request.data['contact_number'],
#             image=request.data['image'],
#             visiting_date=request.data['visiting_date'],
#             visiting_time=request.data['visiting_time'],
#             created_by=logged_in_user,  
#         )
#         lead_visitor.save()

#         print(f'User {logged_in_user.username} created a new LeadVisitor instance.')

        
@csrf_exempt
def getAccompanyingVisitors(request):
    if request.method == 'GET':
        unique_id = request.GET.get('unique_id', '')
        if unique_id:
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
        from_date, to_date = request.GET.get('from_date', ''), request.GET.get('to_date', '')  
        date = request.GET.get('date', '')
        if unique_id:
            lead_visitors = LeadVisitor.objects.filter(unique_id=unique_id).first()
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
            if lead_visitor.valid_till.replace(tzinfo=None) < datetime.datetime.now():
                print(f"Expired: ID {unique_id}")
                return JsonResponse({'message': 'expired'})
            else:
                print(f"Not Expired: ID {unique_id}")
                return JsonResponse({'message': 'not expired'})
        else:
            return JsonResponse({'message': 'not found'})
    else:
        return JsonResponse({'message': f'{request.method} not allowed. Only GET allowed'})

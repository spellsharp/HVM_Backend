from rest_framework import serializers
from .models import LeadVisitor, Accompanying
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token
class LeadVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadVisitor
        fields = '__all__'
        
class AccompanyingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accompanying
        fields = '__all__'
from rest_framework import serializers
from .models import LeadVisitor, Accompanying

class LeadVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadVisitor
        fields = '__all__'
        
class AccompanyingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accompanying
        fields = '__all__'
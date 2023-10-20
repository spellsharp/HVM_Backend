import datetime
from django.http import JsonResponse
from rest_framework import serializers
from .models import LeadVisitor, Accompanying, Receiver
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        print("===============================")
        print(token)
        print("===============================")
        return token
    
class LeadVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadVisitor
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['visiting_date'] = datetime.date.today()
        validated_data['visiting_time'] = datetime.datetime.now().time()
        return super().create(validated_data)
        
class AccompanyingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accompanying
        fields = '__all__'
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    contact_number = serializers.CharField(write_only=True, required=True)
    employee_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name', 'email', 'contact_number', 'employee_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        # TODO: Add other fields after its done
        Receiver.objects.create(username=user.username, created_by=self.context['request'].user, full_name=user.first_name + " " + user.last_name, contact_number = validated_data['contact_number'], employee_id = validated_data['employee_id'])

        return user
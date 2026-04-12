from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8, style = {'input_type':'password'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # extra_kwargs = { 
        #     'id': {'read_only': True} 
        # }        

    def create(self, validated_data):
        user = User.objects.create_user(
            email= validated_data['email'],
            password = validated_data['password'],
            username = validated_data['username']
            )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only =True)
    password = serializers.CharField(write_only= True)

    def validate(self,data):
        user = authenticate(email = data['email'], password = data['password'])
        if user:
            return user
        raise serializers.ValidationError("Invalid email or password")
    
class ProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source = 'user.bio', read_only = True)
    class Meta:
        model = Profile
        fields = ['user','bio','rating', 'problems_solved', 'avatar']
        extra_kwargs={
            'user':{'read_only': True},
            'rating':{'read_only': True},
            'problems_solved':{'read_only': True},
        }
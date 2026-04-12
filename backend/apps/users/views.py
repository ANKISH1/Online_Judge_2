from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile
# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh =RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({'access':str(access), 'refresh':str(refresh)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status = status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): #since this is single object view, so we override get_object instead of get_queryset
        return self.request.user.profile # since onetoone field, we can access directly
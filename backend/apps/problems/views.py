from django.shortcuts import render
from .serializers import ProblemListSerializer, ProblemDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from .models import Problems
# Create your views here.

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProblemDetailSerializer
        return ProblemListSerializer

    def get_queryset(self):
        queryset = Problems.objects.all()
        return queryset
    
    def get_permissions(self):
        if self.request.method =="POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
class ProblemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProblemDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Problems.objects.all()
        return queryset

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]    
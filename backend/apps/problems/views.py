from django.shortcuts import render
from .serializers import ProblemListSerializer, ProblemDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from .models import Problems
from django.core.cache import cache
from rest_framework.views import APIView
from .ai import hint
from rest_framework.response import Response
# Create your views here.

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProblemDetailSerializer
        return ProblemListSerializer

    def get_queryset(self):
        difficulty = self.request.query_params.get('difficulty', 'all')
        cache_key = f"problems_list_{difficulty}"

        cached = cache.get(cache_key)
        if cached:
            return cached
        
        queryset = Problems.objects.all()
        if difficulty!='all':
            queryset = queryset.filter(difficulty = difficulty)
        cache.set(cache_key, queryset, timeout=300)
        return queryset
    
    def get_permissions(self):
        if self.request.method =="POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete_pattern('problems_list_*')
    
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


class HintView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            problem = Problems.objects.get(id = pk)
        except Problems.DoesNotExist:
            return Response({"error": "Problem not found"}, status=404) 
           
        user_code = request.data.get('user_code', '')
        hint_text = hint(problem.description, user_code)

        return Response({"hint": hint_text})
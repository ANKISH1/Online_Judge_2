from django.shortcuts import render
from rest_framework import generics
from .serializers import SubmissionListCreateSerializer, AllSubmissionsSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Submissions

# Create your views here.
class SubmissionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SubmissionListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Submissions.objects.filter(user = self.request.user, problem = self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class AllSubmissionsView(generics.ListAPIView):
    serializer_class = AllSubmissionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Submissions.objects.filter(user = self.request.user)
        return queryset
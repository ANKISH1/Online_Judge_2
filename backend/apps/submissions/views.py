from django.shortcuts import render
from rest_framework import generics
from .serializers import SubmissionListCreateSerializer, AllSubmissionsSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Submissions
from apps.judge.tasks import execute_submission

# Create your views here.
class SubmissionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SubmissionListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Submissions.objects.filter(user = self.request.user, problem = self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        submission = serializer.save(user = self.request.user)
        execute_submission.delay(submission.id)


class AllSubmissionsView(generics.ListAPIView):
    serializer_class = AllSubmissionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Submissions.objects.filter(user = self.request.user).select_related('problem')
        return queryset
from django.urls import path
from .views import SubmissionListCreateAPIView, AllSubmissionsView, SubmissionDetailView

urlpatterns = [
    path('problem/<int:pk>/',SubmissionListCreateAPIView.as_view(), name = 'problem_submission'),
    path('', AllSubmissionsView.as_view(), name = 'all_submissions'),
    path('<int:pk>/', SubmissionDetailView.as_view(), name = 'submission-detail')
]

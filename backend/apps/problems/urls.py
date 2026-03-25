from django.urls import path
from .views import ProblemListCreateAPIView, ProblemDetailAPIView

urlpatterns = [
    path('',ProblemListCreateAPIView.as_view(), name = 'problems'),
    path('<int:pk>/', ProblemDetailAPIView.as_view(),name = 'problem_detail')
]
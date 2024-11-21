from django.urls import path
from . import views  # import views from your app

urlpatterns = [
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_form, name='candidate_form'),
    path('welcome/<str:candidate_code>/', views.welcome, name='welcome'),
]
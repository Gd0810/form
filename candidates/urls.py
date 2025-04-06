from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_form, name='candidate_form'),
    path('custom/<uuid:token>/', views.custom_prefilled_form, name='custom_prefilled_form'),  # New URL with token
    path('welcome/<str:candidate_code>/', views.welcome, name='welcome'),
]
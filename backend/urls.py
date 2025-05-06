from django.urls import path
from . import views  # Import your app's views

urlpatterns = [
    # Define your app's URL patterns here
    path('insulin_chart/', views.scheduling_api, name='insulin_chart'),
    path('schedule/', views.scheduling_api, name='scheduling'),
    path('temprature/', views.temprature_api, name='temprature'),
    path('', views.main_page, name='main_page'),
    
    # Add more paths as needed
]
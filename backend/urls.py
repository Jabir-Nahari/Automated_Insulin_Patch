from django.urls import path
from . import views  # Import your app's views

urlpatterns = [
    # Define your app's URL patterns here
    path('schedule/', views.scheduling_api, name='scheduling'),
    path('', views.main_page, name='main_page'),
    
    # Add more paths as needed
]
from django.urls import path
from . import views  # Import your app's views

urlpatterns = [
    # Define your app's URL patterns here
    path('', views.main_page, name='main_page'),
    path('api/schedule/', views.scheduling_api, name='scheduling'),
    # Add more paths as needed
]
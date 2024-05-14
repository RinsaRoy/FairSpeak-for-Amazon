from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('analysis/', views.analysis, name="analysis"),
    path('bulkreview/', views.bulkreview, name="bulkreview"),
    path('amazon_reviews/', views.amazon_reviews, name='amazon_reviews'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('send-feedback/', views.send_feedback, name='send_feedback'),
]

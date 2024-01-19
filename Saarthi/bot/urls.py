from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save_audio/', views.save_audio, name='save_audio'),
    path('send_text_query/', views.send_text_query, name='send_text_query'),
]

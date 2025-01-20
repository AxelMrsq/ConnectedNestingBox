from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Hourly-data', views.hourlydata, name='hourlydata'),
    path('Recorded-audio', views.recordedaudio, name='recordedaudio'),
    path('About', views.about, name='about'),
    path('App', views.app, name='app')
]
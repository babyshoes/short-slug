from django.urls import path
from . import views

urlpatterns = [
    path('', views.random, name='random'),
    path('custom/', views.custom, name='custom'),
    path('reroute/<slug>', views.reroute, name='reroute'),
    path('stats/<slug>', views.stats, name='stats')
]
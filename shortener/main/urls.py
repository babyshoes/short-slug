from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('<long_url>/', views.random, name='random'),
    path('custom/<long_url>/<short_url>', views.custom, name='custom'),
    path('reroute/<slug>', views.reroute, name='reroute'),
    path('stats/<slug>', views.stats, name='stats')
]
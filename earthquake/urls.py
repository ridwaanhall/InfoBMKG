from django.urls import path
from . import views

# earthquake/urls.py
urlpatterns = [
    path('', views.dashboard_html, name='dashboard-quake'),
    path('latest/', views.latest_html, name='latest-quake'),
    
    # earthquakes
    path('live200/', views.live200_html, name='live200-quake'),
    path('last30felt/', views.last30felt_html, name='last30felt-quake'),
    path('last30/', views.last30_html, name='last30-quake'),
    path('last30tsunami/', views.last30tsunami_html, name='last30tsunami-quake'),
    
    # histories
    path('last3months/', views.last3months_html, name='last3months-quake'),
    path('last5years/', views.last5years_html, name='last5years-quake'),
    path('destructive/', views.destructive_html, name='destructive-quake'),
]
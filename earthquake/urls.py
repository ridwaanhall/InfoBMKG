from django.urls import path
from . import views

# earthquake/urls.py
urlpatterns = [
    path('', views.dashboard_html, name='dashboard-quake'),
    path('latest/', views.latest_html, name='latest-quake'),
    path('live30/', views.live30_html, name='live-30-quake'),
]
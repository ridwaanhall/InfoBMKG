from django.urls import path
from . import views

# earthquake/urls.py
urlpatterns = [
    path('', views.dashboard, name='dashboard-quake'),
    path('latest/', views.latest, name='latest-quake'),
    # other URL patterns
]
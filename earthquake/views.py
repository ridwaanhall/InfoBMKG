import requests
from django.shortcuts import render
from django.conf import settings

BASE_URL = settings.BASE_URL

def dashboard(request):
    return render(request, 'earthquake/dashboard.html')

def latest(request):
    latest = requests.get(f'{BASE_URL}/datagempa.json')
    latest = latest.json()
    coordinates = latest['info']['point']['coordinates']
    longitude, latitude = coordinates.split(',')
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
    }
    return render(request, 'earthquake/latest.html', context)
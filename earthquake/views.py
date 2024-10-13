import requests
from django.shortcuts import render
from django.conf import settings

OUR_URL = settings.OUR_URL

def dashboard(request):
    return render(request, 'earthquake/dashboard.html')

def latest(request):
    latest = requests.get(f'{OUR_URL}/latest/')
    latest = latest.json()
    coordinates = latest['info']['point']['coordinates']
    longitude, latitude = coordinates.split(',')
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
    }
    return render(request, 'earthquake/latest.html', context)
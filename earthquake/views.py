import requests
from django.shortcuts import render
from django.conf import settings

OUR_URL = settings.OUR_URL

def dashboard(request):
    try:
        latest_response = requests.get(f'{OUR_URL}/latest/')
        latest_response.raise_for_status()  # Raise an HTTPError for bad responses
        latest = latest_response.json()
        coordinates = latest['info']['point']['coordinates']
        longitude, latitude = coordinates.split(',')
    except (requests.RequestException, KeyError, ValueError) as e:
        latest = None
        longitude = None
        latitude = None

    fault_indo_world_response = requests.get(f'{OUR_URL}/fault-indo-world/')
    fault_indo_world = fault_indo_world_response.json()
    
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
        'fault_indo_world': fault_indo_world,
    }
    return render(request, 'earthquake/dashboard.html', context)

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
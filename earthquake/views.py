import requests
from django.shortcuts import render
from django.conf import settings

OUR_URL = settings.OUR_URL

def dashboard(request):
    try:
        latest_response = requests.get(f'{OUR_URL}/latest/')
        latest_response.raise_for_status()  # Raise an HTTPError for bad responses
        latest = latest_response.json()
        
        if 'info' in latest and 'point' in latest['info'] and 'coordinates' in latest['info']['point']:
            coordinates = latest['info']['point']['coordinates']
            longitude, latitude = coordinates.split(',')
        else:
            longitude = None
            latitude = None
    except (requests.RequestException, KeyError, ValueError) as e:
        latest = None
        longitude = None
        latitude = None

    fault_indo_world_response = requests.get(f'{OUR_URL}/fault-indo-world/')
    fault_indo_world = fault_indo_world_response.json()
    
    intensity_map_response = requests.get(f'{OUR_URL}/intensity-map/')
    intensity_map = intensity_map_response.json()
    
    narration_response = requests.get(f'{OUR_URL}/latest-narration/')
    narration = narration_response.json()
    
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
        'fault_indo_world': fault_indo_world,
        'intensity_map': intensity_map,
        'narration': narration,
    }
    return render(request, 'earthquake/dashboard.html', context)

def latest(request):
    try:
        latest_response = requests.get(f'{OUR_URL}/latest/')
        latest_response.raise_for_status()  # Raise an HTTPError for bad responses
        latest = latest_response.json()
        
        if 'info' in latest and 'point' in latest['info'] and 'coordinates' in latest['info']['point']:
            coordinates = latest['info']['point']['coordinates']
            longitude, latitude = coordinates.split(',')
        else:
            longitude = None
            latitude = None
    except (requests.RequestException, KeyError, ValueError) as e:
        latest = None
        longitude = None
        latitude = None
    
    images_url_response = requests.get(f'{OUR_URL}/images-url/')
    images_url = images_url_response.json()
    
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
        'images_url': images_url,
    }
    return render(request, 'earthquake/latest.html', context)
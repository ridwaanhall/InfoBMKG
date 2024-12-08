import requests
from django.shortcuts import render
from django.conf import settings

OUR_URL = settings.OUR_URL

def dashboard_html(request):
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
    
    mmi_map_response = requests.get(f'{OUR_URL}/mmi-map/')
    mmi_map = mmi_map_response.json()
    
    narration_response = requests.get(f'{OUR_URL}/latest-narration/')
    narration = narration_response.json()
    
    context = {
        'latest': latest,
        'longitude': longitude,
        'latitude': latitude,
        'fault_indo_world': fault_indo_world,
        'mmi_map': mmi_map,
        'narration': narration,
    }
    return render(request, 'earthquake/dashboard.html', context)

def latest_html(request):
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

def live200_html(request):
    try:
        live200_response = requests.get(f'{OUR_URL}/live200/')
        live200_response.raise_for_status()  # Raise an HTTPError for bad responses
        live200 = live200_response.json()
    except requests.RequestException as e:
        live200 = None
    
    context = {
        'live200': live200,
    }
    return render(request, 'earthquake/live200.html', context)

def last30felt_html(request):
    try:
        last30felt_response = requests.get(f'{OUR_URL}/last30felt/')
        last30felt_response.raise_for_status()  # Raise an HTTPError for bad responses
        last30felt = last30felt_response.json()
    except requests.RequestException as e:
        last30felt = None
    
    context = {
        'last30felt': last30felt,
    }
    return render(request, 'earthquake/last30felt.html', context)

def last30_html(request):
    try:
        last30_response = requests.get(f'{OUR_URL}/last30/')
        last30_response.raise_for_status()  # Raise an HTTPError for bad responses
        last30 = last30_response.json()
    except requests.RequestException as e:
        last30 = None
    
    context = {
        'last30': last30,
    }
    return render(request, 'earthquake/last30.html', context)

def last30tsunami_html(request):
    try:
        last30tsunami_response = requests.get(f'{OUR_URL}/last30tsunami/')
        last30tsunami_response.raise_for_status()  # Raise an HTTPError for bad responses
        last30tsunami = last30tsunami_response.json()
    except requests.RequestException as e:
        last30tsunami = None
    
    context = {
        'last30tsunami': last30tsunami,
    }
    return render(request, 'earthquake/last30tsunami.html', context)

def last3months_html(request):
    try:
        last3months_response = requests.get(f'{OUR_URL}/last3months/')
        last3months_response.raise_for_status()  # Raise an HTTPError for bad responses
        last3months = last3months_response.json()
    except requests.RequestException as e:
        last3months = None
    
    context = {
        'last3months': last3months,
    }
    return render(request, 'earthquake/last3months.html', context)

def last5years_html(request):
    try:
        last5years_response = requests.get(f'{OUR_URL}/last5years/')
        last5years_response.raise_for_status()  # Raise an HTTPError for bad responses
        last5years = last5years_response.json()
    except requests.RequestException as e:
        last5years = None
    
    context = {
        'last5years': last5years,
    }
    return render(request, 'earthquake/last5years.html', context)

def destructive_html(request):
    try:
        destructive_response = requests.get(f'{OUR_URL}/destructive/')
        destructive_response.raise_for_status()  # Raise an HTTPError for bad responses
        destructive = destructive_response.json()
    except requests.RequestException as e:
        destructive = None
    
    context = {
        'destructive': destructive,
    }
    return render(request, 'earthquake/destructive.html', context)
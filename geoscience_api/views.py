import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import base64

BASE_URL = settings.BASE_URL
OUR_URL = settings.OUR_URL

def make_api_request_no_keyword(endpoint):
    api_url = f"{BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            return response.json()
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            return ET.fromstring(response.content)
        elif 'text/html' in content_type:
            soup = BeautifulSoup(response.content, 'html.parser')
            narration_text = soup.get_text(separator='\n', strip=True)
            return {'narration': narration_text}
        elif 'text/plain' in content_type:
            return {'narration': response.text.strip()}
        elif 'application/octet-stream' in content_type:
            return response.content
        elif 'image/jpeg' in content_type or 'image/png' in content_type:
            return response.content  # Return raw image bytes
        else:
            return {'error': f'Unsupported content type: {content_type}'}
    except requests.exceptions.HTTPError as http_err:
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': 'Connection error occurred', 'details': str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': 'Request timed out', 'details': str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        return {'error': 'An error occurred', 'details': str(req_err)}

# documentation
class Documentation(APIView):
    def get(self, _):
        return Response({
            'endpoints': {
            'latest': {
                'url': f'{OUR_URL}/latest/',
                'note': 'Latest Earthquake'
            },
            'latest-narration': {
                'url': f'{OUR_URL}/latest-narration/',
                'note': 'Latest Earthquake Narration'
            },
            'latest-focal': {
                'url': f'{OUR_URL}/latest-focal/',
                'note': 'Latest Earthquake Focal'
            },
            'images-url': {
                'url': f'{OUR_URL}/images-url/',
                'note': 'Images URL'
            },
            'impact-list': {
                'url': f'{OUR_URL}/impact-list/',
                'note': 'Impact List Image'
            },
            'intensity-map': {
                'url': f'{OUR_URL}/intensity-map/',
                'note': 'Intensity Map Image'
            },
            'station-list-MMI': {
                'url': f'{OUR_URL}/station-list-MMI/',
                'note': 'Station List MMI Image'
            },
            'location-map': {
                'url': f'{OUR_URL}/location-map/',
                'note': 'Location Map Image'
            },
            'mmi-map': {
                'url': f'{OUR_URL}/mmi-map/',
                'note': 'Map MMI Image'
            },
            'last3months': {
                'url': f'{OUR_URL}/last3months/',
                'note': 'Earthquakes < 3 Months'
            },
            'last5years': {
                'url': f'{OUR_URL}/last5years/',
                'note': 'Earthquakes < 5 Years'
            },
            'seismic-sensor-bmkg': {
                'url': f'{OUR_URL}/seismic-sensor-bmkg/',
                'note': 'Seismic Sensor BMKG'
            },
            'seismic-sensor-global': {
                'url': f'{OUR_URL}/seismic-sensor-global/',
                'note': 'Seismic Sensor Global'
            },
            'destructive-epicenter': {
                'url': f'{OUR_URL}/destructive-epicenter/',
                'note': 'Destructive Earthquake Epicenter'
            },
            'last30': {
                'url': f'{OUR_URL}/last30/',
                'note': 'Last 30 Events > 5 Magnitude'
            },
            'last30felt': {
                'url': f'{OUR_URL}/last30felt/',
                'note': 'Last 30 Felt Earthquake'
            },
            'last30stunami': {
                'url': f'{OUR_URL}/last30stunami',
                'note': 'Last 30 Tsunami Event'
            },
            'live30': {
                'url': f'{OUR_URL}/live30',
                'note': 'Live Earthquake'
            },
            'indo-fault-lines': {
                'url': f'{OUR_URL}/indo-fault-lines/',
                'note': 'Indo Fault Lines GeoJSON'
            },
            'fault-indo-world': {
                'url': f'{OUR_URL}/fault-indo-world/',
                'note': 'Fault Indo World GeoJSON'
            }
            }
        })

# latests
class SingleLatestQuake(APIView): # Latest Earthquake
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        return Response(latest)

class LatestQuakeNarration(APIView):  # Latest Earthquake Narration
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            narration_endpoint = f"{eventid}_narasi.txt"
            narration_response = make_api_request_no_keyword(narration_endpoint)

            if 'narration' in narration_response:
                soup = BeautifulSoup(narration_response['narration'], 'html.parser')
                cleaned_narration = soup.get_text(separator='\n').strip()
                return Response(
                    {
                        'cleaned_narration': cleaned_narration,
                        'original_narration': narration_response['narration']
                    }
                )
            else:
                return Response({'error': 'Invalid narration format or data not found'})
        
        return Response({'error': 'Event ID not found in latest earthquake data'})
    
class LatestQuakeFocal(APIView):  # Latest Earthquake Focal
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            focal_endpoint = f"{eventid}_focal.json"
            focal_response = make_api_request_no_keyword(focal_endpoint)
            return Response(focal_response)
        else:
            return Response({'error': 'Event ID not found in latest earthquake data'})

# histories
class LessThan3MonthsQuakes(APIView): # Earthquakes < 3 Months
    def get(self, _):
        less_than_3_months = make_api_request_no_keyword('3mgempaQL.json')
        return Response(less_than_3_months)
    
class LessThan5YearsQuakes(APIView): # Earthquakes < 5 Years
    def get(self, _):
        less_than_5_years = make_api_request_no_keyword('histori.json')
        return Response(less_than_5_years)

# sensors
class SeismicSensorBMKG(APIView):
    def get(self, _):
        seismic_sensor_BMKG = make_api_request_no_keyword('sensor_seismic.json')
        return Response(seismic_sensor_BMKG)
    
class SeismicSensorGlobal(APIView):
    def get(self, _):
        seismic_sensor_global = make_api_request_no_keyword('sensor_global.json')
        return Response(seismic_sensor_global)

# new menu
class DestructiveEarthquakesEpicenter(APIView): # Destructive Earthquake Epicenter
    def get(self, _):
        destructive = make_api_request_no_keyword('katalog_gempa.json')
        return Response(destructive)

# events
class Last30Events(APIView):  # > 5 Magnitude
    def get(self, _):
        events = make_api_request_no_keyword('last30event.xml')
        if isinstance(events, ET.Element):

            alert_details = {
                "identifier": events.find('{urn:oasis:names:tc:emergency:cap:1.2}identifier').text,
                "sender": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sender').text,
                "sent": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sent').text,
                "status": events.find('{urn:oasis:names:tc:emergency:cap:1.2}status').text,
                "msgType": events.find('{urn:oasis:names:tc:emergency:cap:1.2}msgType').text,
                "scope": events.find('{urn:oasis:names:tc:emergency:cap:1.2}scope').text,
                "code": events.find('{urn:oasis:names:tc:emergency:cap:1.2}code').text,
                "info": []
            }

            for info in events.findall('{urn:oasis:names:tc:emergency:cap:1.2}info'):
                event_info = {
                    'event': info.find('{urn:oasis:names:tc:emergency:cap:1.2}event').text,
                    'date': info.find('{urn:oasis:names:tc:emergency:cap:1.2}date').text,
                    'time': info.find('{urn:oasis:names:tc:emergency:cap:1.2}time').text,
                    'point': {
                        'coordinates': info.find('{urn:oasis:names:tc:emergency:cap:1.2}point').find('{urn:oasis:names:tc:emergency:cap:1.2}coordinates').text
                    },
                    'latitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}latitude').text,
                    'longitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}longitude').text,
                    'magnitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}magnitude').text,
                    'depth': info.find('{urn:oasis:names:tc:emergency:cap:1.2}depth').text,
                    'area': info.find('{urn:oasis:names:tc:emergency:cap:1.2}area').text,
                    'eventid': info.find('{urn:oasis:names:tc:emergency:cap:1.2}eventid').text,
                    'potential': info.find('{urn:oasis:names:tc:emergency:cap:1.2}potential').text,
                    'subject': info.find('{urn:oasis:names:tc:emergency:cap:1.2}subject').text,
                    'headline': info.find('{urn:oasis:names:tc:emergency:cap:1.2}headline').text,
                    'description': info.find('{urn:oasis:names:tc:emergency:cap:1.2}description').text,
                    'instruction': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction').text,
                    'shakemap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}shakemap').text,
                    'timesent': info.find('{urn:oasis:names:tc:emergency:cap:1.2}timesent').text,
                }

                alert_details["info"].append(event_info)

            return Response(alert_details)

        return Response(events)
    
class Last30FeltEvents(APIView): # Felt Earthquake
    def get(self, _):
        events = make_api_request_no_keyword('last30feltevent.xml')
        if isinstance(events, ET.Element):

            alert_details = {
                "identifier": events.find('{urn:oasis:names:tc:emergency:cap:1.2}identifier').text,
                "sender": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sender').text,
                "sent": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sent').text,
                "status": events.find('{urn:oasis:names:tc:emergency:cap:1.2}status').text,
                "msgType": events.find('{urn:oasis:names:tc:emergency:cap:1.2}msgType').text,
                "scope": events.find('{urn:oasis:names:tc:emergency:cap:1.2}scope').text,
                "code": events.find('{urn:oasis:names:tc:emergency:cap:1.2}code').text,
                "info": []
            }

            for info in events.findall('{urn:oasis:names:tc:emergency:cap:1.2}info'):
                event_info = {
                    'event': info.find('{urn:oasis:names:tc:emergency:cap:1.2}event').text,
                    'date': info.find('{urn:oasis:names:tc:emergency:cap:1.2}date').text,
                    'time': info.find('{urn:oasis:names:tc:emergency:cap:1.2}time').text,
                    'point': {
                        'coordinates': info.find('{urn:oasis:names:tc:emergency:cap:1.2}point').find('{urn:oasis:names:tc:emergency:cap:1.2}coordinates').text
                    },
                    'latitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}latitude').text,
                    'longitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}longitude').text,
                    'magnitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}magnitude').text,
                    'depth': info.find('{urn:oasis:names:tc:emergency:cap:1.2}depth').text,
                    'area': info.find('{urn:oasis:names:tc:emergency:cap:1.2}area').text,
                    'eventid': info.find('{urn:oasis:names:tc:emergency:cap:1.2}eventid').text,
                    'potential': info.find('{urn:oasis:names:tc:emergency:cap:1.2}potential').text,
                    'subject': info.find('{urn:oasis:names:tc:emergency:cap:1.2}subject').text,
                    'headline': info.find('{urn:oasis:names:tc:emergency:cap:1.2}headline').text,
                    'description': info.find('{urn:oasis:names:tc:emergency:cap:1.2}description').text,
                    'instruction': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction').text,
                    'felt': info.find('{urn:oasis:names:tc:emergency:cap:1.2}felt').text,
                    'shakemap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}shakemap').text,
                    'timesent': info.find('{urn:oasis:names:tc:emergency:cap:1.2}timesent').text,
                }

                alert_details["info"].append(event_info)

            return Response(alert_details)

        return Response(events)
    
class Last30TsunamiEvents(APIView): # Tsunami Event
    def get(self, _):
        events = make_api_request_no_keyword('last30tsunamievent.xml')
        if isinstance(events, ET.Element):

            alert_details = {
                "identifier": events.find('{urn:oasis:names:tc:emergency:cap:1.2}identifier').text,
                "sender": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sender').text,
                "sent": events.find('{urn:oasis:names:tc:emergency:cap:1.2}sent').text,
                "status": events.find('{urn:oasis:names:tc:emergency:cap:1.2}status').text,
                "msgType": events.find('{urn:oasis:names:tc:emergency:cap:1.2}msgType').text,
                "scope": events.find('{urn:oasis:names:tc:emergency:cap:1.2}scope').text,
                "code": events.find('{urn:oasis:names:tc:emergency:cap:1.2}code').text,
                "info": []
            }

            for info in events.findall('{urn:oasis:names:tc:emergency:cap:1.2}info'):
                event_info = {
                    'event': info.find('{urn:oasis:names:tc:emergency:cap:1.2}event').text,
                    'date': info.find('{urn:oasis:names:tc:emergency:cap:1.2}date').text,
                    'time': info.find('{urn:oasis:names:tc:emergency:cap:1.2}time').text,
                    'point': {
                        'coordinates': info.find('{urn:oasis:names:tc:emergency:cap:1.2}point').find('{urn:oasis:names:tc:emergency:cap:1.2}coordinates').text
                    },
                    'latitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}latitude').text,
                    'longitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}longitude').text,
                    'magnitude': info.find('{urn:oasis:names:tc:emergency:cap:1.2}magnitude').text,
                    'depth': info.find('{urn:oasis:names:tc:emergency:cap:1.2}depth').text,
                    'area': info.find('{urn:oasis:names:tc:emergency:cap:1.2}area').text,
                    'eventid': info.find('{urn:oasis:names:tc:emergency:cap:1.2}eventid').text,
                    'potential': info.find('{urn:oasis:names:tc:emergency:cap:1.2}potential').text,
                    'subject': info.find('{urn:oasis:names:tc:emergency:cap:1.2}subject').text,
                    'headline': info.find('{urn:oasis:names:tc:emergency:cap:1.2}headline').text,
                    'description': info.find('{urn:oasis:names:tc:emergency:cap:1.2}description').text,
                    'instruction': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction').text,
                    'shakemap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}shakemap').text,
                    'wzmap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}wzmap').text,
                    'ttmap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}ttmap').text,
                    'sshmap': info.find('{urn:oasis:names:tc:emergency:cap:1.2}sshmap').text,
                    'instruction1': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction1').text,
                    'instruction2': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction2').text,
                    'instruction3': info.find('{urn:oasis:names:tc:emergency:cap:1.2}instruction3').text,
                    'timesent': info.find('{urn:oasis:names:tc:emergency:cap:1.2}timesent').text,
                }
                
                alert_details["info"].append(event_info)
                
            return Response(alert_details)
        
        return Response(events)

class Live200Events(APIView): # Live Earthquake
    def get(self, _):
        events = make_api_request_no_keyword('live30event.xml')
        if isinstance(events, ET.Element):
            alert_details = {
                "info": []
            }

            for gempa in events.findall('gempa'):
                event_info = {
                    'eventid': gempa.find('eventid').text,
                    'status': gempa.find('status').text,
                    'datetime': gempa.find('waktu').text,
                    'latitude': gempa.find('lintang').text,
                    'longitude': gempa.find('bujur').text,
                    'depth': gempa.find('dalam').text,
                    'magnitude': gempa.find('mag').text,
                    'fokal': gempa.find('fokal').text,
                    'area': gempa.find('area').text,
                }

                alert_details["info"].append(event_info)

            return Response(alert_details)

        return Response(events)

# geojson
class GeoJsonAPIView(APIView):
    def get(self, request, endpoint):
        geojson_data = make_api_request_no_keyword(endpoint)
        
        if isinstance(geojson_data, dict) and 'error' in geojson_data:
            return Response(geojson_data)

        if isinstance(geojson_data, bytes):
            try:
                geojson_data = json.loads(geojson_data.decode('utf-8'))
            except json.JSONDecodeError as json_err:
                return Response({'error': 'Failed to decode GeoJSON', 'details': str(json_err)})

        return Response(geojson_data)

class IndoFaultsLines(GeoJsonAPIView):
    def get(self, request):
        return super().get(request, 'indo_faults_lines.geojson')

class FaultsIndoWorld(GeoJsonAPIView):
    def get(self, request):
        return super().get(request, 'fault_indo_world.geojson')

# images (jpg and png)
class ImageAPIView(APIView):
    def get_image(self, endpoint):
        image = make_api_request_no_keyword(endpoint)
        if isinstance(image, bytes):
            content_type = 'image/jpeg' if endpoint.endswith('.jpg') else 'image/png'
            base64_image = base64.b64encode(image).decode('utf-8')
            image_url = f"data:{content_type};base64,{base64_image}"
            return image_url
        return None

class ImpactList(ImageAPIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            impactlist_endpoint = f"{eventid}_rev/impact_list.jpg"
            image_url = self.get_image(impactlist_endpoint)
            if image_url:
                return Response({'image_url': image_url, 'message': 'Impact list image retrieved successfully'})
        return Response({'error': 'Event ID not found in latest earthquake data'})

class IntensityMap(ImageAPIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            intensitylogo_endpoint = f"{eventid}_rev/intensity_logo.jpg"
            image_url = self.get_image(intensitylogo_endpoint)
            if image_url:
                return Response({'image_url': image_url, 'message': 'Intensity map image retrieved successfully'})
        return Response({'error': 'Event ID not found in latest earthquake data'})

class StationListMMI(ImageAPIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            stationlist_endpoint = f"{eventid}_rev/stationlist_MMI.jpg"
            image_url = self.get_image(stationlist_endpoint)
            if image_url:
                return Response({'image_url': image_url, 'message': 'Station list MMI image retrieved successfully'})
        return Response({'error': 'Event ID not found in latest earthquake data'})

class LocationMap(ImageAPIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            locmap_endpoint = f"{eventid}_rev/loc_map.png"
            image_url = self.get_image(locmap_endpoint)
            if image_url:
                return Response({'image_url': image_url, 'message': 'Location map image retrieved successfully'})
        return Response({'error': 'Event ID not found in latest earthquake data'})

class MMIMap(ImageAPIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            map_mmi_endpoint = f"{eventid}.mmi.jpg"
            image_url = self.get_image(map_mmi_endpoint)
            if image_url:
                return Response({'image_url': image_url, 'message': 'Map MMI image retrieved successfully'})
        return Response({'error': 'Event ID not found in latest earthquake data'})

class ImagesURL(APIView):
    def get(self, _):
        latest = make_api_request_no_keyword('datagempa.json')
        if 'info' in latest and latest['info']:
            eventid = latest['info']['eventid']
            impactlist_endpoint = f"{eventid}_rev/impact_list.jpg"
            intensitylogo_endpoint = f"{eventid}_rev/intensity_logo.jpg"
            stationlist_endpoint = f"{eventid}_rev/stationlist_MMI.jpg"
            locmap_endpoint = f"{eventid}_rev/loc_map.png"
            map_mmi_endpoint = f"{eventid}.mmi.jpg"

            impactlist_url = ImpactList().get_image(impactlist_endpoint)
            intensitylogo_url = IntensityMap().get_image(intensitylogo_endpoint)
            stationlist_url = StationListMMI().get_image(stationlist_endpoint)
            locmap_url = LocationMap().get_image(locmap_endpoint)
            mmi_url = MMIMap().get_image(map_mmi_endpoint)

            images = {
                'impactlist_url': impactlist_url,
                'intensitylogo_url': intensitylogo_url,
                'stationlist_url': stationlist_url,
                'locmap_url': locmap_url,
                'mmi_url': mmi_url
            }

            available_images = {key: value for key, value in images.items() if value}
            unavailable_images = [key for key, value in images.items() if not value]

            message = 'Images retrieved successfully for: ' + ', '.join(available_images.keys())
            if unavailable_images:
                message += '. Images not found for: ' + ', '.join(unavailable_images)

            return Response({
                **images,
                'message': message
            })
        return Response({'error': 'Event ID not found in latest earthquake data'})

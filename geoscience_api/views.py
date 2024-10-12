from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

BASE_URL = settings.BASE_URL

def make_api_request_no_keyword(endpoint):
    api_url = f"{BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        # print("Content-Type:", content_type)

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

# maps
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

            # print("Narration Response Headers:", narration_response)

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

            # Extracting alert-level details
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
                # For each event info
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
    
class Last30FeltEvent(APIView): # Felt Earthquake
    def get(self, _):
        events = make_api_request_no_keyword('last30feltevent.xml')
        if isinstance(events, ET.Element):

            # Extracting alert-level details
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
                # For each event info
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
    
class Last30TsunamiEvent(APIView): # Tsunami Event
    def get(self, _):
        events = make_api_request_no_keyword('last30tsunamievent.xml')
        if isinstance(events, ET.Element):

            # Extracting alert-level details
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
                # For each event info
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

class Live30Event(APIView): # Live Earthquake
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

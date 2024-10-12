from django.urls import path
from . import views

# geoscience_api/urls.py
urlpatterns = [
    # maps
    path('latest/', views.SingleLatestQuake.as_view(), name='latest-quake'),
    path('latest-narration/', views.LatestQuakeNarration.as_view(), name='latest-quake-narration'),
    path('last3months/', views.LessThan3MonthsQuakes.as_view(), name='last-3-months-quake'),
    path('last5years/', views.LessThan5YearsQuakes.as_view(), name='last-5-years-quake'),
    
    # sensors
    path('seismic-sensor-bmkg/', views.SeismicSensorBMKG.as_view(), name='seismic-sensor-bmkg'),
    path('seismic-sensor-global/', views.SeismicSensorGlobal.as_view(), name='seismic-sensor-global'),
    
    # new menu
    path('destructive-epicenter/', views.DestructiveEarthquakesEpicenter.as_view(), name='destructive-earthquakes-epicenter'),
    
    # events
    path('last30/', views.Last30Events.as_view(), name='last-30-events'),
    path('last30felt/', views.Last30FeltEvent.as_view(), name='last-30-felt'),
    path('last30stunami', views.Last30TsunamiEvent.as_view(), name='last-30-felt'),
    path('live30', views.Live30Event.as_view(), name='live-30-event'),
    
    # geojson
    path('indo-fault-lines/', views.IndoFaultsLines.as_view(), name='indo-fault-lines'),
    path('fault-indo-world/', views.FaultsIndoWorld.as_view(), name='fault-indo-world'),
]
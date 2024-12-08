from django.urls import path
from . import views

# geoscience_api/urls.py
urlpatterns = [
    # documentation
    path('', views.Documentation.as_view(), name='documentation'),
    
    # latests
    path('latest/', views.SingleLatestQuake.as_view(), name='latest-quake'),
    path('latest-narration/', views.LatestQuakeNarration.as_view(), name='latest-quake-narration'),
    path('latest-focal/', views.LatestQuakeFocal.as_view(), name='latest-quake-focal'),
    
    # images url
    path('images-url/', views.ImagesURL.as_view(), name='images-url'),
    
    # images
    path('impact-list/', views.ImpactList.as_view(), name='impact-list'),
    path('intensity-map/', views.IntensityMap.as_view(), name='intensity-map'),
    path('station-list-MMI/', views.StationListMMI.as_view(), name='station-list-mmi'),
    path('location-map/', views.LocationMap.as_view(), name='location-map'),
    path('mmi-map/', views.MMIMap.as_view(), name='mmi-map'),

    # histories
    path('last3months/', views.LessThan3MonthsQuakes.as_view(), name='last3months'),
    path('last5years/', views.LessThan5YearsQuakes.as_view(), name='last5years'),
    
    # sensors
    path('seismic-sensor-bmkg/', views.SeismicSensorBMKG.as_view(), name='seismic-sensor-bmkg'),
    path('seismic-sensor-global/', views.SeismicSensorGlobal.as_view(), name='seismic-sensor-global'),
    
    # new menu
    path('destructive/', views.DestructiveEarthquakesEpicenter.as_view(), name='destructive'),
    
    # events
    path('live200/', views.Live200Events.as_view(), name='live200'),
    path('last30felt/', views.Last30FeltEvents.as_view(), name='last30felt'),
    path('last30/', views.Last30Events.as_view(), name='last30'),
    path('last30tsunami/', views.Last30TsunamiEvents.as_view(), name='last30tsunami'),
    
    # geojson
    path('indo-fault-lines/', views.IndoFaultsLines.as_view(), name='indo-fault-lines'),
    path('fault-indo-world/', views.FaultsIndoWorld.as_view(), name='fault-indo-world'),
]

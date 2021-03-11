from django.urls import path, include
 
urlpatterns = [
    path('', include('ca_camera.urls')),
]
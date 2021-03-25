from django.conf import settings
from django_hosts import patterns, host
 
host_patterns = patterns(
    '',
    host(r'', 'config.home_urls', name='home'),
    host(r'admin', settings.ROOT_URLCONF, name='admin'),
    host(r'camera', 'config.ca_camera_urls', name='camera'),
    host(r'lens', 'config.ca_lens_urls', name='lens'),
)
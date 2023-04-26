
from django.urls import path

from .views import *

app_name = 'sensor'
urlpatterns = [
    path('busanQ/list/', busanQlists),
    path('humidity/list/', humiditylists),
    path('iaq/list/', iaqlists),
    path('dust/list/', dustlists),
    path('dust/data/', dust_data_per_time),
    path('humidity/data/', humidity_data),

    path('airquality/post/', post_dust_density),
    path('airquality/data/', air_quality_data),

    path('anomaly/email/', anomaly_email),
    path('react/sendingEmail/', sendingEmail),

    path('dust/switch/create/', dust_switch_create),
    path('dust/switch/modify/', dust_switch_modify),
    path('dust/switch/get/', dust_switch_get),
    path('api/light/switch/modify/', ard_light_switch_modify),

    path('iaq/csv/upload/', upload_csv_file),
    path('iaq/upload/', upload_iaq_csv),
]

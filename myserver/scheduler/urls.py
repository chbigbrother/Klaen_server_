
from django.urls import path

from .views import *

app_name = 'scheduler'
urlpatterns = [
    path('time/', max_site_per_time),
    path('schedule/list/', schedulelists),
    path('busan/data/', busan_data_list),
    path('humidity/data/', humidity_data),
    path('humidity/list/', humiditylists),
    path('temperature/list/', temperaturelists),
    path('dust/list/', dustlists),
    path('dust/data/', dust_data_per_time),
    path('settings/', schedule_settings),
    path('save/settings/', save_schedule_settings),
    path('search/type/', search_type),
    path('airquality/data/', air_quality_data),
    path('airquality/post/', post_dust_density),
    path('anomaly/email/', anomaly_email),
    path('dust/switch/create/', dust_switch_create),
    path('dust/switch/modify/', dust_switch_modify),
    path('dust/switch/modify/adu/', ard_dust_switch_modify),
    path('dust/switch/get/', dust_switch_get),
    path('api/dust/switch/get/', app_dust_switch_get),
    path('react/sendingEmail/', sendingEmail),
    # path('react/deviceSwitchStatus/', deviceSwitchStatus),

]

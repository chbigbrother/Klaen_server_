
from django.urls import path

from .views import *

app_name = 'scheduler'
urlpatterns = [
    path('time/', max_site_per_time),
    path('busan/data/', busan_data_list),
    path('other/factors/', other_factor_lists),
    path('sunrise/data/', get_sunrise_data),

    path('settings/', schedule_settings),
    path('save/settings/', save_schedule_settings),
    path('search/type/', search_type),

    path('dust/switch/modify/adu/', ard_dust_switch_modify),
    path('api/dust/switch/get/', app_dust_switch_get),

    # path('react/deviceSwitchStatus/', deviceSwitchStatus),

]

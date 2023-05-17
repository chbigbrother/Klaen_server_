
from django.urls import path

from .views import *

app_name = 'scheduler'
urlpatterns = [
    path('time/', max_site_per_time),
    path('other/factors/', OtherFactors.as_view()),
    path('sunrise/data/', get_sunrise_data),

    path('settings/', SchedulerSettings.as_view(), name="list"),
    # Example: /order/ORD001/update/
    path('<str:pk>/edit/', SchedulerSettingsEdit.as_view(), name="update"),
    path('<str:pk>/delete/', SchedulerSettingsDelete.as_view(), name="delete"),
    path('add/', SchedulerSettingsAdd.as_view(), name="add"),
    path('search/type/', search_type),

    path('dust/switch/modify/adu/', ard_dust_switch_modify),
    path('api/dust/switch/get/', app_dust_switch_get),

    # path('react/deviceSwitchStatus/', deviceSwitchStatus),

]

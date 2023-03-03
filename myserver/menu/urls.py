from django.urls import path

from .views import *

app_name = 'menu'
urlpatterns = [
    path('settings/', menu_settings),
    path('create/', menu_list_create),
    path('create/new/', menu_create),
    path('api/lists/', menu_lists),
    path('api/lists/byuser/', menu_lists_by_user),
    path('setting/modify/', menu_setting_modify),
    path('api/setting/modify/', app_menu_setting_modify)
]
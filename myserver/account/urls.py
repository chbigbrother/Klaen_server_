
from django.urls import path

from .views import *

app_name = 'account'
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('login/api', login_api),
    path('logout/api', logout_api),
    path('user/list/api', userlists_api),
    path('user/list/', UserSearch.as_view()),
    path('user/stat/', userstats),
    path('user/stat/list/', userstat_data),
    path('user/group/update/', user_group_update),
    path('', home),
]

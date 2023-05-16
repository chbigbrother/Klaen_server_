from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from account.models import *
import datetime, json
from datetime import timedelta
from menu.models import MenuLists, MenuCheckLists
from scheduler.models import HumiditySensor, AirQuality, DustSensor, DustSensorSwitch
from forms.utils import dbLocation
import dateutil.parser
import pymongo

# 127.0.0.1:8000/
class Home(ListView):
    template_name = 'index.html'
    context_object_name = 'dust_list'

    def get_queryset(self):
        # login을 통해서 확인된 user는 session을 통해 user.id를 넘겨 받았다.
        user_id = self.request.session.get('user')
        user = User.objects.get(id=user_id)
        dateFrom, dateTo = get_dates(self.request)
        get_date = datetime.datetime.today() - timedelta(hours=1)
        get_date = get_date.strftime("%Y-%m-%d")
        get_date = get_date + " T00:00:00.000Z"
        get_date = dateutil.parser.parse(get_date)

        self.user_id = user
        self.dateFrom = dateFrom
        self.dateTo = dateTo

        return DustSensor.objects.filter(timestamp__gte=get_date).order_by('-timestamp')

def get_dates(request):
    date = datetime.datetime.today() - timedelta(days=3)

    if 'dateFrom' in request.GET:
        date_from = datetime.datetime.strptime(request.GET['dateFrom'], "%Y-%m-%d")
        date_to = datetime.datetime.strptime(request.GET['dateTo'], "%Y-%m-%d")
    else:
        date_from = date
        date_to = datetime.datetime.today()

    return date_from.strftime("%Y-%m-%d"), date_to.strftime("%Y-%m-%d")
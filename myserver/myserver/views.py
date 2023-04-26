from django.http import HttpResponse
from django.shortcuts import render, redirect
from account.models import *
import datetime, json
from datetime import timedelta
from menu.models import MenuLists, MenuCheckLists
from forms.utils import dbLocation
import dateutil.parser
import pymongo
# 127.0.0.1:8000/

client = pymongo.MongoClient(dbLocation)
db = client['server_db']
dustdb = db['scheduler_dustsensor']
# 127.0.0.1:8000/
def home(request):
    # login을 통해서 확인된 user는 session을 통해 user.id를 넘겨 받았다.
    user_id = request.session.get('user')
    user = User.objects.get(id=user_id)
    dateFrom, dateTo = get_dates(request)
    get_date = datetime.datetime.today() - timedelta(hours=1)
    get_date = get_date.strftime("%Y-%m-%d")
    get_date = get_date + " T00:00:00.000Z"
    get_date = dateutil.parser.parse(get_date)
    # menus = MenuCheckLists.objects.filter(user_id_id=user_id).order_by('id')
    # menu_result = []
    # menu_dict = {}
    # cnt = 0
    # for i in menus:
    #     cnt += 1
    #     menu_dict[cnt] = i.menu_yn
    # menu_result.append(menu_dict)
    latest_data = dustdb.find({
        'timestamp': {'$gte': get_date},
    }).limit(20).sort("id", -1)

    dust__result = []
    for i in latest_data:
        dust_dict = {}
        dust_dict['humidity'] = i['humidity']
        dust_dict['temperature'] = i['temperature']
        dust_dict['dustDensity'] = i['dustDensity']
        dust_dict['timestamp'] = (i['timestamp'] + datetime.timedelta(hours=9)).strftime("%Y-%m-%d, %H:%M:%S")
        dust__result.append(dust_dict)

    print('user:::: ', user_id)
    data = {
        'user_id': user.username,
        'dateFrom': dateFrom,
        'dateTo': dateTo,
        'airq_list': dust__result,
        'app_name': 'company',
        'path': '회사정보 / 설비현황검색'
    }

    return render(request, 'index.html', data)

def get_dates(request):
    date = datetime.datetime.today() - timedelta(days=3)

    if 'dateFrom' in request.GET:
        date_from = datetime.datetime.strptime(request.GET['dateFrom'], "%Y-%m-%d")
        date_to = datetime.datetime.strptime(request.GET['dateTo'], "%Y-%m-%d")
    else:
        date_from = date
        date_to = datetime.datetime.today()

    return date_from.strftime("%Y-%m-%d"), date_to.strftime("%Y-%m-%d")
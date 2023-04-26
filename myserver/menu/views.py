from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from account.models import User
from forms.views import id_generate
from datetime import timedelta
from forms.utils import dbLocation
import json, datetime
import pymongo
# Create your views here.
def menu_list_create(request):

    # MenuLists.objects.create(
    #     menu_id = "MN_007",
    #     menu_name="Lab Humidity Sensor",
    #     menu_parent="0",
    #     menu_link = "/",
    #     menu_order = "1",
    # )

    MenuCheckLists.objects.create(
        menu_id = MenuLists.objects.get(menu_id="MN_007"),
        user_id = User.objects.get(username="test"),
        menu_yn="y"
    )

    return JsonResponse({"message": 'success'})

def menu_settings(request):
    template_name = 'menu_settings.html'
    user_id = request.session.get('user')
    date = datetime.datetime.today() - timedelta(days=3)
    settings = MenuCheckLists.objects.filter(user_id_id=user_id).order_by('id')
    set_result = []

    for i in settings:
        sdict = {}
        sdict['menu_id'] = MenuLists.objects.get(id=i.menu_id_id).menu_id
        sdict['menu_name'] = MenuLists.objects.get(id=i.menu_id_id).menu_name
        sdict['menu_yn'] = i.menu_yn
        set_result.append(sdict)

    date = {
        "settings": set_result,
        'dateFrom': date.strftime("%Y-%m-%d"),

        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)


def menu_lists(request):
    mlists = MenuLists.objects.all().order_by('id')
    result = []
    for i in mlists:
        m_dict = {}
        m_dict['id'] = i.id
        m_dict['menu_id'] = i.menu_id
        m_dict['menu_name'] = i.menu_name
        m_dict['menu_parent'] = i.menu_parent
        m_dict['menu_link'] = i.menu_link
        m_dict['menu_order'] = i.menu_order
        result.append(m_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default))

@csrf_exempt
def menu_lists_by_user(request):

    user_id = request.GET['user']
    user = User.objects.get(username=user_id)
    date = datetime.datetime.today() - timedelta(days=3)
    settings = MenuCheckLists.objects.filter(user_id_id=user.id).order_by('id')
    set_result = []

    for i in settings:
        sdict = {}
        sdict['menu_id'] = MenuLists.objects.get(id=i.menu_id_id).menu_id
        sdict['menu_name'] = MenuLists.objects.get(id=i.menu_id_id).menu_name
        sdict['menu_yn'] = i.menu_yn
        set_result.append(sdict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(set_result, default=json_default))

client = pymongo.MongoClient(dbLocation)
db = client['server_db']
menuCheckListDB = db['menu_menuchecklists']

@csrf_exempt
def menu_setting_modify(request):

    if request.method == 'POST':
        menu_id = request.POST['menu_id']
        menu_yn = request.POST['menu_yn']

    if menu_yn == 'y':
        menu_yn = 'n'
    else:
        menu_yn = 'y'
    menu_id = MenuLists.objects.get(menu_id=menu_id).id
    menuCheckListDB.update_one({"menu_id": menu_id}, {"$set": {"menu_yn": menu_yn}})

    return JsonResponse({"message": 'success'})

@api_view(['GET', 'POST'])
def app_menu_setting_modify(request):
    request = json.loads(request.body)

    menu_id = request['menu_id']
    menu_yn = request['menu_yn']

    if menu_yn == 'y':
        menu_yn = 'n'
    else:
        menu_yn = 'y'

    menu_id = MenuLists.objects.get(menu_id=menu_id).id
    menuCheckListDB.update_one({"menu_id": menu_id}, {"$set": {"menu_yn": menu_yn}})

    return JsonResponse({"message": 'success'})

@api_view(['GET', 'POST'])
def menu_create(request):
    request = json.loads(request.body)

    menu_name = request['menu_name']
    menu_link = request['menu_link']
    username = request['username']

    id_count = MenuLists.objects.all().order_by('id').last()
    if id_count is None:
        int_id = 0
    else:
        int_id = id_count.menu_id[3:]
    str_id = id_generate('MN_', int_id)

    MenuLists.objects.create(
        menu_id = str_id,
        menu_name=menu_name,
        menu_parent="0",
        menu_link = menu_link,
        menu_order = "1",
    )

    MenuCheckLists.objects.create(
        menu_id=MenuLists.objects.get(menu_id=str_id),
        username=User.objects.get(username=username),
        menu_yn="y"
    )

    return JsonResponse({"message": 'success'})
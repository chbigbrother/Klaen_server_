...
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse, QueryDict
import datetime
from datetime import timedelta
import json, datetime
from urllib.parse import urlencode, unquote, quote_plus
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework.decorators import api_view
from background_task import background
from logging import getLogger
from forms.utils import dbLocation
from django.http.response import HttpResponse
from .models import *
from myserver.views import get_dates
from forms.views import send_email
import pymongo
import dateutil.parser
from pytz import timezone, utc
import json
...

to_year = int(datetime.datetime.today().strftime("%Y"))
to_month = int(datetime.datetime.today().strftime("%m"))
to_day = int(datetime.datetime.today().strftime("%d"))


def send_mail_():
    # 날짜 셋팅
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    date = nowDate.split('-')

    print("OPERATING")

serviceKey = "FXEr17kvrd8Whbj9vNbm%2FRAkUbRnRsERDGr7%2BjdrHjYU6ZJKnNixEYbxwfF4BXuLhvewafwgoITp4BE%2BWK9org%3D%3D"
serviceKeyDecoded = unquote(serviceKey, 'UTF-8')
def get_busan_air_qualily():
    print("OPERATING")
    url = "http://apis.data.go.kr/6260000/AirQualityInfoService/getAirQualityInfoClassifiedByStation"
    queryParams = '?' + 'serviceKey=' + serviceKey + '&resultType=json'

    request = requests.get(url + queryParams)
    soup = BeautifulSoup(request.content, 'html.parser')
    soup = json.loads(str(soup))
    air_data = []

    for i in range(len(soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'])):
        indiv = []
        in_data = {}
        in_data['sites'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['site']
        in_data['areaIndex'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['areaIndex']
        in_data['controlnumber'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i][
            'controlnumber']
        in_data['repItem'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['repItem']
        in_data['repVal'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['repVal']
        in_data['repCai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['repCai']
        in_data['so2'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['so2']
        in_data['so2Cai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['so2Cai']
        in_data['no2'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['no2']
        in_data['no2Cai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['no2Cai']
        in_data['o3'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['o3']
        in_data['o3Cai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['o3Cai']
        in_data['co'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['co']
        in_data['coCai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['coCai']
        in_data['pm25'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['pm25']
        in_data['pm25Cai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['pm25Cai']
        in_data['pm10'] = int(soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['pm10'])
        in_data['pm10Cai'] = soup['getAirQualityInfoClassifiedByStation']['body']['items']['item'][i]['pm10Cai']
        # indiv.append(in_data)
        air_data.append(in_data)

    for i in range(len(air_data)):
        AirQuality.objects.create(
            site=air_data[i]['sites'],
            areaIndex=air_data[i]['areaIndex'],
            controlnumber=air_data[i]['controlnumber'],
            repItem=air_data[i]['repItem'],
            repVal=air_data[i]['repVal'],
            repCai=air_data[i]['repCai'],
            so2=air_data[i]['so2'],
            so2Cai=air_data[i]['so2Cai'],
            no2=air_data[i]['no2'],
            no2Cai=air_data[i]['no2Cai'],
            o3=air_data[i]['o3'],
            o3Cai=air_data[i]['o3Cai'],
            co=air_data[i]['co'],
            coCai=air_data[i]['coCai'],
            pm25=air_data[i]['pm25'],
            pm25Cai=air_data[i]['pm25Cai'],
            pm10=air_data[i]['pm10'],
            pm10Cai=air_data[i]['pm10Cai'],
        )

def other_factor_lists(request):
    template_name = 'other_factors.html'
    hum_list = HumiditySensor.objects.filter().order_by("-created_at")
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "hum_list": hum_list,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

def get_weather_data(date):
    if date == None:
        startDt = datetime.datetime.today() - timedelta(days=3)
        endDt = datetime.datetime.today() - timedelta(days=1)
        startDt = startDt.strftime("%Y%m%d")
        endDt = endDt.strftime("%Y%m%d")
    else:
        startDt = date.replace('-', '')[:8]
        endDt = date.replace('-', '')[:8]

    stnIds = '159'
    serviceKey = "FXEr17kvrd8Whbj9vNbm%2FRAkUbRnRsERDGr7%2BjdrHjYU6ZJKnNixEYbxwfF4BXuLhvewafwgoITp4BE%2BWK9org%3D%3D"
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8')
    url = "https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
    queryParams = '?' + 'serviceKey=' + serviceKey + '&dataCd=ASOS&dateCd=DAY&startDt=' + startDt + '&endDt=' + endDt + '&stnIds=' + stnIds + '&dataType=json'
    # & dataCd = ASOS & dateCd = DAY & startDt = 20100101 & endDt = 20100102 & stnIds = 159

    request = requests.get(url + queryParams)
    soup = BeautifulSoup(request.content, 'html.parser')
    soup = json.loads(str(soup))

    outData = []
    for i in range(len(soup['response']['body']['items']['item'])):
        data_dict = {}

        rainfall = soup['response']['body']['items']['item'][i]['sumRn']
        avgtemp = soup['response']['body']['items']['item'][i]['avgTa']
        if len(rainfall) > 0:
            rainfall = 'Y'
        else:
            rainfall = 'N'
        data_dict['rainfall'] = rainfall
        data_dict['avgtemp'] = avgtemp
        outData.append(data_dict)

    return outData



def get_sunrise_data(date):
    if date == None:
        startDt = datetime.datetime.today() - timedelta(days=3)
        endDt = datetime.datetime.today() - timedelta(days=1)
        startDt = startDt.strftime("%Y%m%d")
        endDt = endDt.strftime("%Y%m%d")

    serviceKey = "FXEr17kvrd8Whbj9vNbm/RAkUbRnRsERDGr7+jdrHjYU6ZJKnNixEYbxwfF4BXuLhvewafwgoITp4BE+WK9org=="
    url = 'http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo'
    # queryParams = '?' + 'serviceKey=' + serviceKey + '&locdate=20230501&location=서울&dataType=json'
    # & dataCd = ASOS & dateCd = DAY & startDt = 20100101 & endDt = 20100102 & stnIds = 159
    # request = requests.get(url + queryParams)
    params = {'serviceKey': serviceKey, 'locdate': '20230501', 'location': '서울'}
    response = requests.get(url, params=params)
    content = response.text
    xml_obj = BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.findAll('item')

    # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
    row_list = []  # 행값
    name_list = []  # 열이름값
    value_list = []  # 데이터값

    # xml 안의 데이터 수집
    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        # 첫째 행 데이터 수집
        for j in range(0, len(columns)):
            if i == 0:
                # 컬럼 이름 값 저장
                name_list.append(columns[j].name)
            # 컬럼의 각 데이터 값 저장
            if j == 15 or j == 16:
                value_list.append(columns[j].text.replace(' ', ''))
        # 각 행의 value값 전체 저장
        row_list.append(value_list)
        # 데이터 리스트 값 초기화
        value_list = []
    print(row_list)


    return response.content



client = pymongo.MongoClient(dbLocation)
db = client['server_db']
airdb = db['scheduler_airquality']
humdb = db['scheduler_humiditysensor']
tempdb = db['scheduler_temperaturesensor']
dustdb = db['scheduler_dustsensor']
dust_switch_db = db['scheduler_dustsensorswitch']
settingsdb = db['scheduler_schedulesettings']

# recent busan air quality data
def max_site_per_time(request):

    get_date = datetime.datetime.today() - timedelta(hours=1)
    get_date = get_date.strftime("%Y%m%d%H")

    latest_data = airdb.find({
        'controlnumber': get_date
    })
    result_dict = {}
    result = []
    locations = []

    for i in latest_data:
        air_dict = {}
        locations.append(i['site'])
        air_dict['site'] = i['site']
        air_dict['areaIndex'] = i['areaIndex']
        air_dict['controlnumber'] = i['controlnumber']
        air_dict['repItem'] = i['repItem']
        air_dict['repVal'] = i['repVal']
        air_dict['repCai'] = i['repCai']
        air_dict['so2'] = i['so2']
        air_dict['so2Cai'] = i['so2Cai']
        air_dict['no2'] = i['no2']
        air_dict['no2Cai'] = i['no2Cai']
        air_dict['o3'] = i['o3']
        air_dict['o3Cai'] = i['o3Cai']
        air_dict['co'] = i['co']
        air_dict['coCai'] = i['coCai']
        air_dict['pm25'] = i['pm25']
        air_dict['pm25Cai'] = i['pm25Cai']
        air_dict['pm10'] = i['pm10']
        air_dict['pm10Cai'] = i['pm10Cai']
        result.append(air_dict)

    loc_set = set(locations)
    locations = list(loc_set)
    fin_result = []
    lng = 0
    for i in range(len(locations)):
        for j in range(len(result)):
            if lng == len(locations):
                break;
            else:
                fin_result.append(result[j])
                lng += 1


    result_dict['data'] = fin_result
    result_dict['locations'] = locations

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result_dict, default=json_default)) # demo_task(soup)

# busan air quality data search
def post_air_quality(request):

    latest_data = airdb.find({
        'created_at': {
            '$gt': datetime.datetime(to_year, to_month, to_day)
        }
    })

    backgroundColor = [
        'rgba(245, 238, 248)',
        'rgba(215, 189, 226)',
        'rgba(169, 204, 227)',
        'rgba(127, 179, 213)',
        'rgba(163, 228, 215)',
        'rgba(118, 215, 196)',
        'rgba(171, 235, 198)',
        'rgba(130, 224, 170)',
        'rgba(249, 231, 159)',
        'rgba(248, 196, 113)',
    ];

    result_dict = {}
    result = []
    locations = []

    for i in latest_data:
        air_dict = {}
        locations.append(i['site'])
        air_dict['site'] = i['site']
        air_dict['areaIndex'] = i['areaIndex']
        air_dict['controlnumber'] = i['controlnumber']
        air_dict['repItem'] = i['repItem']
        air_dict['repVal'] = i['repVal']
        air_dict['repCai'] = i['repCai']
        air_dict['so2'] = i['so2']
        air_dict['so2Cai'] = i['so2Cai']
        air_dict['no2'] = i['no2']
        air_dict['no2Cai'] = i['no2Cai']
        air_dict['o3'] = i['o3']
        air_dict['o3Cai'] = i['o3Cai']
        air_dict['co'] = i['co']
        air_dict['coCai'] = i['coCai']
        air_dict['pm25'] = i['pm25']
        air_dict['pm25Cai'] = i['pm25Cai']
        air_dict['pm10'] = i['pm10']
        air_dict['pm10Cai'] = i['pm10Cai']
        result.append(air_dict)
    loc_set = set(locations)
    locations = list(loc_set)

    bgc = []
    for i in range(len(result)):
        for j in range(len(locations)):
            bgc.append(backgroundColor[j])

    result_dict['data'] = result
    result_dict['locations'] = locations
    result_dict['bgc'] = bgc

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result_dict, default=json_default)) # demo_task(soup)

# scheduling timer info
def schedule_setting():
    timer = ScheduleSettings.object.all().order_by('id').last()
    # ScheduleSettings.objects.create(
        # timer="1"
    # )
    return timer

# busan air quality data list
def busan_data_list(request):
    airq_list = AirQuality.objects.all()
    result_dict = {}
    result = []

    for i in airq_list:
        air_dict = {}
        air_dict['site'] = i.site
        air_dict['areaIndex'] = i.areaIndex
        air_dict['controlnumber'] = i.controlnumber
        air_dict['repItem'] = i.repItem
        air_dict['repVal'] = i.repVal
        air_dict['repCai'] = i.repCai
        air_dict['so2'] = i.so2
        air_dict['so2Cai'] = i.so2Cai
        air_dict['no2'] = i.no2
        air_dict['no2Cai'] = i.no2Cai
        air_dict['o3'] = i.o3
        air_dict['o3Cai'] = i.o3Cai
        air_dict['co'] = i.co
        air_dict['coCai'] = i.coCai
        air_dict['pm25'] = i.pm25
        air_dict['pm25Cai'] = i.pm25Cai
        air_dict['pm10'] = i.pm10
        air_dict['pm10Cai'] = i.pm10Cai
        result.append(air_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default))

# schedule settings HTML
def schedule_settings(request):
    template_name = 'schedule_settings.html'
    settings = ScheduleSettings.objects.all()
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "settings": settings,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

# save schedule settings
@csrf_exempt
def save_schedule_settings(request):

    # POST 로 받아온 값 dict 로 담기
    if request.method == 'POST':
        request = json.loads(request.body)
        type = request['type']
        timer = request['timer']
        command_type = request['command_type']

    if command_type == "create":
        ScheduleSettings.objects.update_or_create(
            type=type,
            timer=timer,
        )
    else:
        sch_update = ScheduleSettings.objects.get(type=type)
        sch_update.timer = timer
        sch_update.save()
    return JsonResponse({"message": 'success'})

@csrf_exempt
def search_type(request):
    type = request.GET.get('type')
    set_lists = settingsdb.find({
        'type': type,
    })
    result = []
    for i in set_lists:
        air_dict = {}
        air_dict['type'] = i['type']
        air_dict['timer'] = i['timer']
        result.append(air_dict)
    
    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default))  # demo_task(soup)

## arduino and react native app api ##

# @api_view(['GET', 'POST'])
@csrf_exempt
def ard_dust_switch_modify(request):

    request = json.loads(request.body)

    humidity = request['humidity']
    temperature = request['temperature']
    dust = request['dust']
    lighting = request['lighting']

    if humidity == "1":
        humidity = "on"
    else:
        humidity = "off"
    if temperature == "1":
        temperature = "on"
    else:
        temperature = "off"
    if dust == "1":
        dust = "on"
    else:
        dust = "off"

    dust_switch_db.update_one({"ids": 1}, {"$set": {
        "humidityS": humidity,
        "temperatureS": temperature,
        "dustDensityS": dust,
        "lighting": lighting}})

    return JsonResponse({"message": 'success'})

    
def app_dust_switch_get(request):

    ds = DustSensorSwitch.objects.get(ids=1)
    if ds.humidityS == "on":
        hum = "1"
    else:
        hum = "0"
    if ds.temperatureS == "on":
        temp = "1"
    else:
        temp = "0"
    if ds.dustDensityS == "on":
        dust = "1"
    else:
        dust = "0"
    result = []
    result_dict = {}
    result_dict['hum'] = hum
    result_dict['temp'] = temp
    result_dict['dust'] = dust
    result_dict['lighting'] = str(ds.lighting)
    result.append(result_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default)) # demo_task(soup)


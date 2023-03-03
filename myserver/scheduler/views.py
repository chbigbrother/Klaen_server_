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
from django.http.response import HttpResponse
from .models import *
from myserver.views import get_dates
from forms.views import send_email
import pymongo
import dateutil.parser
from pytz import timezone, utc

#import json
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

client = pymongo.MongoClient('mongodb://203.247.166.29:27017')
db = client['server_db']
airdb = db['scheduler_airquality']
humdb = db['scheduler_humiditysensor']
tempdb = db['scheduler_temperaturesensor']
dustdb = db['scheduler_dustsensor']
dust_switch_db = db['scheduler_dustsensorswitch']
settingsdb = db['scheduler_schedulesettings']
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

def schedule_setting():
    timer = ScheduleSettings.object.all().order_by('id').last()
    # ScheduleSettings.objects.create(
        # timer="1"
    # )
    return timer

def schedulelists(request):
    template_name = 'schedule_list.html'
    airq_list = AirQuality.objects.all()
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "airq_list": airq_list,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

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



def humiditylists(request):
    template_name = 'humidity_list.html'
    hum_list = HumiditySensor.objects.filter().order_by("-created_at")
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "hum_list": hum_list,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

def temperaturelists(request):
    template_name = 'temperature_list.html'
    temp_list = TemperatureSensor.objects.filter().order_by("-created_at")
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "hum_list": temp_list,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

def dustlists(request):
    template_name = 'dust_list.html'
    # airq_list = DustSensor.objects.all().order_by("-timestamp")

    if 'dateFrom' in request.GET:
        dateFrom = request.GET['dateFrom']
        dateTo = request.GET['dateTo']
        print(dateFrom)
    else:
        dateFrom, dateTo = get_dates(request)

    date_from = dateFrom + " T00:00:00.000Z"
    date_from = dateutil.parser.parse(date_from)
    date_to = dateTo + " T23:59:59.000Z"
    date_to = dateutil.parser.parse(date_to)

    airq_list = dustdb.find({
        'timestamp':
            {
                '$gte': date_from,
                '$lt': date_to
            },
    }).sort("id", -1) # .limit(20).sort("id", -1)

    dust__result = []
    for i in airq_list:
        dust_dict = {}
        dust_dict['humidity'] = i['humidity']
        dust_dict['temperature'] = i['temperature']
        dust_dict['dustDensity'] = i['dustDensity']
        dust_dict['timestamp'] = (i['timestamp'] + datetime.timedelta(hours=9)).strftime("%Y-%m-%d, %H:%M:%S")
        dust__result.append(dust_dict)

    data = {
        "airq_list": dust__result,
        'dateFrom': dateFrom,
        'dateTo': dateTo,
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, data)

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


def get_humidity():
    print("HUM_OPERATING")
    url = "https://vpw.my.id/microcontroller/postData.json"

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    soup = json.loads(str(soup))

    HumiditySensor.objects.create(
        moisture=soup[-1]['moistureSensor'],
    )

def humidity_data(request):
    hum_data = HumiditySensor.objects.all()
    hum_result = []
    for i in hum_data:
        hum_dict = {}
        hum_dict['moisture'] = i.moisture
        hum_dict['timestamp'] = i.created_at.strftime("%Y-%m-%d, %H:%M:%S")
        hum_result.append(hum_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(hum_result, default=json_default)) # demo_task(soup)

@csrf_exempt
def post_dust_density(request):

    if request.method == 'POST':
        humidity = request.POST['humidity']
        temperature = request.POST['temperature']
        dustDensity = request.POST['dustDensity'].split("\x00")[0]
        datetime = request.POST['datetime']

        ds = DustSensorSwitch.objects.get(ids=1)

        if ds.dustDensityS == "off":
            DustSensor.objects.create(
                humidity=humidity,
                temperature=temperature,
                datetime=datetime,
            )
        elif ds.humidityS == "off":
            DustSensor.objects.create(
                temperature=temperature,
                dustDensity=dustDensity,
                datetime=datetime,
            )
        elif ds.temperatureS == "off":
            DustSensor.objects.create(
                humidity=humidity,
                dustDensity=dustDensity,
                datetime=datetime
            )
        elif ds.dustDensityS == "off" and ds.humidityS == "off":
            DustSensor.objects.create(
                temperature=temperature,
                datetime=datetime,
            )
        elif ds.dustDensityS == "off" and ds.temperatureS == "off":
            DustSensor.objects.create(
                humidity=humidity,
                datetime=datetime,
            )
        elif ds.humidityS == "off" and ds.temperatureS == "off":
            DustSensor.objects.create(
                dustDensity=dustDensity,
                datetime=datetime,
            )
        else:
            DustSensor.objects.create(
                humidity=humidity,
                temperature=temperature,
                dustDensity=dustDensity,
                datetime=datetime,
            )

    return HttpResponse("success!")

def get_air_quality():
    print("AIR_QUALITY_OPERATING")
    url = "https://vpw.my.id/microcontroller/sensorData.json"

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    soup = json.loads(str(soup))
    ds = DustSensorSwitch.objects.get(ids=1)

    if ds.dustDensityS == "off":
        DustSensor.objects.create(
            humidity=soup[-1]['humidity'],
            temperature=soup[-1]['temperature'],
            datetime=soup[-1]['datetime'],
        )
    elif ds.humidityS == "off":
        DustSensor.objects.create(
            temperature = soup[-1]['temperature'],
            dustDensity = soup[-1]['dustDensity'].split("\x00")[0],
            datetime = soup[-1]['datetime'],
        )
    elif ds.temperatureS == "off":
        DustSensor.objects.create(
            humidity=soup[-1]['humidity'],
            dustDensity=soup[-1]['dustDensity'].split("\x00")[0],
            datetime=soup[-1]['datetime'],
        )
    elif ds.dustDensityS == "off" and ds.humidityS == "off":
        DustSensor.objects.create(
            temperature=soup[-1]['temperature'],
            datetime=soup[-1]['datetime'],
        )
    elif ds.dustDensityS == "off" and ds.temperatureS == "off":
        DustSensor.objects.create(
            humidity=soup[-1]['humidity'],
            datetime=soup[-1]['datetime'],
        )
    elif ds.humidityS == "off" and ds.temperatureS == "off":
        DustSensor.objects.create(
            dustDensity=soup[-1]['dustDensity'].split("\x00")[0],
            datetime=soup[-1]['datetime'],
        )
    else:
        DustSensor.objects.create(
            humidity=soup[-1]['humidity'],
            temperature=soup[-1]['temperature'],
            dustDensity=soup[-1]['dustDensity'].split("\x00")[0],
            datetime=soup[-1]['datetime'],
        )

def air_quality_data(request):
    dust_data = DustSensor.objects.all().order_by("-timestamp")
    dust_result = []
    for i in dust_data:
        dust_dict = {}
        dust_dict['humidity'] = i.humidity
        dust_dict['temperature'] = i.temperature
        dust_dict['dustDensity'] = i.dustDensity
        dust_dict['timestamp'] = (i.timestamp + datetime.timedelta(hours=9)).strftime("%Y-%m-%d, %H:%M:%S")
        dust_result.append(dust_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(dust_result, default=json_default)) # demo_task(soup)

def dust_data_per_time(request):

    get_date = datetime.datetime.today() - timedelta(hours=1)
    get_date = get_date.strftime("%Y-%m-%d")
    get_date = get_date + " T00:00:00.000Z"
    get_date = dateutil.parser.parse(get_date)

    latest_data = dustdb.find({
        'timestamp': {'$gte': get_date},
    }).limit(20).sort("id", -1)

    result_dict = {}
    result = []

    for i in latest_data:
        air_dict = {}
        air_dict['humidity'] = i['humidity']
        air_dict['temperature'] = i['temperature']
        air_dict['dustDensity'] = i['dustDensity']
        air_dict['timestamp'] = (i['timestamp'] + datetime.timedelta(hours=9)).strftime("%Y-%m-%d, %H:%M:%S")
        result.append(air_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default)) # demo_task(soup)

@csrf_exempt
def humidity_data_backup(request):

    if request.method == 'POST':
        # data = JSONParser().parse(request)
        username = request.POST['username']
        password = request.GET['password']

    return HttpResponse("")

@csrf_exempt
def anomaly_email(request):

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        to_m = request.POST['to']
    from_m = "pknubrother@gmail.com"

    send_email(subject, message, from_m, to_m)

    return JsonResponse({"message": 'success'})

#new sending email API
# sending email API
@csrf_exempt
def sendingEmail(request):
    if(request.method == "POST"):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        to = body['to']
        subject = body['subject']
        contents = body['contents']
        from_m = "pknubrother@gmail.com"
        #recipient = body['recipient']
        # to = request.POST.get('toemail')
        # content = request.POST.get(content)
        send_mail(
            #subject
            subject,
            #message
            contents,
            #from email
            from_m,
            #recipient list
            [to]
        )
        return JsonResponse({'message': 'success'})

def dust_switch_create(request):

    DustSensorSwitch.objects.create(
        ids = 1,
        humidityS="on",
        temperatureS="on",
        dustDensityS="on",
    )

    return JsonResponse({"message": 'success'})

@csrf_exempt
def dust_switch_modify(request):

    if request.method == 'POST':
        on_off = request.POST['on_off']
    type = on_off.split('-')[0]
    on_off = on_off.split('-')[1]
    if type == "hum":
        dust_switch_db.update_one({"ids": 1}, {"$set": {"humidityS": on_off}})
    if type == "temp":
        dust_switch_db.update_one({"ids": 1}, {"$set": {"temperatureS": on_off}})
    if type == "dust":
        dust_switch_db.update_one({"ids": 1}, {"$set": {"dustDensityS": on_off}})
    if type == "light":
        dust_switch_db.update_one({"ids": 1}, {"$set": {"lighting": on_off}})


    return JsonResponse({"message": 'success'})

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

def dust_switch_get(request):

    ds = DustSensorSwitch.objects.get(ids=1)
    result = []

    result_dict = {}
    result_dict['hum'] = 'hum-' + ds.humidityS
    result_dict['temp'] = 'temp-' + ds.temperatureS
    result_dict['dust'] = 'dust-' + ds.dustDensityS
    result_dict['lighting'] = 'light-' + ds.lighting
    result.append(result_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default)) # demo_task(soup)
    
    
    
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
    result_dict['lighting'] = ds.lighting
    result.append(result_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default)) # demo_task(soup)


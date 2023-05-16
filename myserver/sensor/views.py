...
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.core.files import File as DjangoFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from django.http.response import HttpResponse
import json, datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from rest_framework.decorators import api_view
from forms.utils import dbLocation
from forms.models import FileUploadCsv
from .models import *
from myserver.views import get_dates
from scheduler.views import *
from scheduler.views import get_weather_data
from scheduler.models import HumiditySensor, AirQuality, DustSensor, DustSensorSwitch
from forms.views import send_email
import pymongo
import dateutil.parser
import json

...
# Create your views here.

client = pymongo.MongoClient(dbLocation)
db = client['server_db']
airdb = db['scheduler_airquality']
humdb = db['scheduler_humiditysensor']
tempdb = db['scheduler_temperaturesensor']
dustdb = db['scheduler_dustsensor']
dust_switch_db = db['scheduler_dustsensorswitch']
settingsdb = db['scheduler_schedulesettings']


# korea air quality HTML
# Data Search/Korea Air Quality
class KoreaAirLists(ListView):

    template_name = 'korea_air_list.html'
    context_object_name = 'airq_list'

    def get_queryset(self):
        if 'dateFrom' in self.request.GET:
            dateFrom = self.request.GET.get('dateFrom')
            dateTo = self.request.GET.get('dateTo')
        else:
            dateFrom, dateTo = get_dates(self.request)

        date_from = dateFrom + " T00:00:00.000Z"
        date_from = dateutil.parser.parse(date_from)
        date_to = dateTo + " T23:59:59.000Z"
        date_to = dateutil.parser.parse(date_to)

        self.dateFrom = dateFrom
        self.dateTo = dateTo

        return AirQuality.objects.filter(created_at__range=[date_from, date_to]).order_by("-created_at")


# iaq list HTML
# Data Mining/IAQ Data
class IaqDataLists(ListView):

    template_name = 'iaq_list.html'

    def get_queryset(self, **kwargs):

        if 'dateFrom' in self.request.GET:
            dateFrom = self.request.GET.get('dateFrom') # ['dateFrom']
            dateTo = self.request.GET.get('dateTo') # ['dateTo']
        else:
            dateFrom, dateTo = get_dates(self.request)

        date_from = dateFrom + " T00:00:00.000Z"
        date_from = dateutil.parser.parse(date_from)
        date_to = dateTo + " T23:59:59.000Z"
        date_to = dateutil.parser.parse(date_to)

        self.dateFrom = dateFrom
        self.dateTo = dateTo

        return IaqData.objects.filter(created_at__range=[date_from, date_to]).order_by("-created_at")

# GET humidity lists
def get_humidity():
    print("HUM_OPERATING")
    url = "https://vpw.my.id/microcontroller/postData.json"

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    soup = json.loads(str(soup))

    HumiditySensor.objects.create(
        moisture=soup[-1]['moistureSensor'],
    )


# humidity data JSON
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

    return HttpResponse(json.dumps(hum_result, default=json_default))  # demo_task(soup)


# air sensors HTML
# Data Search/Air Sensors
class AirSensors(ListView):
    template_name = 'air_sensors.html'
    context_object_name = 'dust_list'
    selected_menu = 'Air Sensors'

    def get_queryset(self, **kwargs):

        if 'dateFrom' in self.request.GET:
            dateFrom = self.request.GET.get('dateFrom') # ['dateFrom']
            dateTo = self.request.GET.get('dateTo') # ['dateTo']
        else:
            dateFrom, dateTo = get_dates(self.request)

        date_from = dateFrom + " T00:00:00.000Z"
        date_from = dateutil.parser.parse(date_from)
        date_to = dateTo + " T23:59:59.000Z"
        date_to = dateutil.parser.parse(date_to)

        self.dateFrom = dateFrom
        self.dateTo = dateTo

        return DustSensor.objects.filter(timestamp__range=[date_from, date_to]).order_by('-timestamp')


# ARDU save dust sensor data
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


# get air quality data JSON
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

    return HttpResponse(json.dumps(dust_result, default=json_default))  # demo_task(soup)


# get dust data per time JSON
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

    return HttpResponse(json.dumps(result, default=json_default))  # demo_task(soup)


@csrf_exempt
def anomaly_email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        to_m = request.POST['to']
    from_m = "pknubrother@gmail.com"

    send_email(subject, message, from_m, to_m)

    return JsonResponse({"message": 'success'})


# new sending email API
# sending email API
@csrf_exempt
def sendingEmail(request):
    if (request.method == "POST"):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        to = body['to']
        subject = body['subject']
        contents = body['contents']
        from_m = "pknubrother@gmail.com"
        # recipient = body['recipient']
        # to = request.POST.get('toemail')
        # content = request.POST.get(content)
        send_mail(
            # subject
            subject,
            # message
            contents,
            # from email
            from_m,
            # recipient list
            [to]
        )
        return JsonResponse({'message': 'success'})


def dust_switch_create(request):
    DustSensorSwitch.objects.create(
        ids=1,
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


def dust_switch_get(request):
    ds = DustSensorSwitch.objects.get(ids=1)
    result = []

    result_dict = {}
    result_dict['hum'] = 'hum-' + ds.humidityS
    result_dict['temp'] = 'temp-' + ds.temperatureS
    result_dict['dust'] = 'dust-' + ds.dustDensityS
    result_dict['lighting'] = 'light-' + str(ds.lighting)
    result.append(result_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(result, default=json_default))  # demo_task(soup)


@api_view(['GET', 'POST'])
def ard_light_switch_modify(request):
    ds = DustSensorSwitch.objects.get(ids=1)
    result = []
    lighting = ds.lighting

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps({"lighting": lighting}, default=json_default))  # demo_task(soup)


# csv file upload
def upload_csv_file(request):
    if request.method == 'POST':
        form = FileUploadCsv(request.POST, request.FILES)
        FileUploadCsv.objects.update_or_create(
            title=request.POST,
            file=request.FILES['file'],
        )
        return JsonResponse({"message": 'success'})
    else:
        form = FileUploadCsv()
    return JsonResponse({"message": request.FILES})


# Draw table after reading csv file
def upload_iaq_csv(request):
    readFile = request.FILES['file'];
    # readFile = FileUploadCsv.objects.all().order_by('-id').last()
    print(readFile);
    read = pd.read_csv('./media/' + str(readFile), encoding='UTF8')

    data_list = []
    #
    for col in read.columns:
        col = read[['Name', 'MAC Address', 'IAQ Score', 'PM 10', 'PM 2.5', 'PM 1.0', 'CO2', 'TVOC',
                    'Temperature', 'Humidity', 'Time']]

        for row in range(int(col.size / 11)):
            weather = get_weather_data(str(col.loc[[row], ['Time']].values).replace('[', '').replace(']', '').replace("'", ''))
            IaqData.objects.create(
                macAddress=str(col.loc[[row], ['MAC Address']].values).replace('[', '').replace(']', '').replace("'",''),
                iaqScore=str(col.loc[[row], ['IAQ Score']].values).replace('[', '').replace(']', '').replace("'", ''),
                pm10=str(col.loc[[row], ['PM 10']].values).replace('[', '').replace(']', '').replace("'", ''),
                pm25=str(col.loc[[row], ['PM 2.5']].values).replace('[', '').replace(']', '').replace("'", ''),
                pm1=str(col.loc[[row], ['PM 1.0']].values).replace('[', '').replace(']', '').replace("'", ''),
                co2=str(col.loc[[row], ['CO2']].values).replace('[', '').replace(']', '').replace("'", ''),
                voc=str(col.loc[[row], ['TVOC']].values).replace('[', '').replace(']', '').replace("'", ''),
                temp=str(col.loc[[row], ['Temperature']].values).replace('[', '').replace(']', '').replace("'", ''),
                humd=str(col.loc[[row], ['Humidity']].values).replace('[', '').replace(']', '').replace("'", ''),
                outAvgTemp=weather[0]['avgtemp'],
                rainfall=weather[0]['rainfall'],
                time=str(col.loc[[row], ['Time']].values).replace('[', '').replace(']', '').replace("'", ''),
            )
        break;

    return JsonResponse({"message": 'success'})


def test_ddd(request):
    return "yes"
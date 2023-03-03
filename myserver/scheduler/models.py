from django.db import models

# Create your models here.
class AirQuality(models.Model):
    site = models.CharField(max_length=255)
    areaIndex = models.FloatField(null=True)
    controlnumber = models.CharField(max_length=120)
    repItem = models.CharField(max_length=120)
    repVal = models.FloatField(null=True)
    repCai = models.CharField(max_length=120)
    so2 = models.FloatField(null=True)
    so2Cai = models.CharField(max_length=120)
    no2 = models.FloatField(null=True)
    no2Cai = models.CharField(max_length=120)
    o3 = models.FloatField(null=True)
    o3Cai = models.CharField(max_length=120)
    co = models.FloatField(null=True)
    coCai = models.CharField(max_length=120)
    pm25 = models.FloatField(null=True)
    pm25Cai = models.CharField(max_length=120)
    pm10 = models.FloatField(null=True)
    pm10Cai = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    modified_at = models.DateTimeField(auto_now=True)  # 수정일자

class ScheduleSettings(models.Model):
    type = models.CharField(max_length=255)
    timer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=False)  # 생성일자
    modified_at = models.DateTimeField(auto_now=False)  # 수정일자

class HumiditySensor(models.Model):
    moisture=models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자

class DustSensor(models.Model):
    humidity=models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    dustDensity = models.FloatField(null=True)
    datetime = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # 생성일자

class DustSensorSwitch(models.Model):
    ids = models.FloatField(null=True)
    humidityS = models.CharField(max_length=4, null=True)
    temperatureS = models.CharField(max_length=4, null=True)
    dustDensityS = models.CharField(max_length=4, null=True)
    lighting = models.CharField(max_length=4, null=True)
    created_at = models.DateTimeField(auto_now_add=False)  # 생성일자
    modified_at = models.DateTimeField(auto_now_add=True)  # 수정일자
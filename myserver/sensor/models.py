from django.db import models

# Create your models here.
class IaqData(models.Model):
    ids = models.FloatField(null=True)
    macAddress = models.CharField(max_length=120, null=True)
    iaqScore = models.FloatField(null=True)
    pm10 = models.FloatField(null=True)
    pm25 = models.FloatField(null=True)
    pm1 = models.FloatField(null=True)
    co2 = models.FloatField(null=True)
    voc = models.FloatField(null=True)
    temp = models.FloatField(null=True)
    humd = models.FloatField(null=True)
    outAvgTemp = models.FloatField(null=True)
    rainfall = models.CharField(max_length=2, null=True)
    time = models.CharField(max_length=120, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자













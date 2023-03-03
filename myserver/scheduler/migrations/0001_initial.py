# Generated by Django 3.2.8 on 2023-01-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=255)),
                ('areaIndex', models.FloatField(null=True)),
                ('controlnumber', models.CharField(max_length=120)),
                ('repItem', models.CharField(max_length=120)),
                ('repVal', models.FloatField(null=True)),
                ('repCai', models.CharField(max_length=120)),
                ('so2', models.FloatField(null=True)),
                ('so2Cai', models.CharField(max_length=120)),
                ('no2', models.FloatField(null=True)),
                ('no2Cai', models.CharField(max_length=120)),
                ('o3', models.FloatField(null=True)),
                ('o3Cai', models.CharField(max_length=120)),
                ('co', models.FloatField(null=True)),
                ('coCai', models.CharField(max_length=120)),
                ('pm25', models.FloatField(null=True)),
                ('pm25Cai', models.CharField(max_length=120)),
                ('pm10', models.FloatField(null=True)),
                ('pm10Cai', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DustSensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity', models.FloatField(null=True)),
                ('temperature', models.FloatField(null=True)),
                ('dustDensity', models.FloatField(null=True)),
                ('datetime', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DustSensorSwitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.FloatField(null=True)),
                ('humidityS', models.CharField(max_length=4, null=True)),
                ('temperatureS', models.CharField(max_length=4, null=True)),
                ('dustDensityS', models.CharField(max_length=4, null=True)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HumiditySensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moisture', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('timer', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
        ),
    ]

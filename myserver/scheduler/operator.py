from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from scheduler.views import *
from scheduler.models import ScheduleSettings

def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    dust_timer = ScheduleSettings.objects.get(type='dustSensor')
    dust_timer = dust_timer.timer
    dust_timer = '*/' + dust_timer

    @scheduler.scheduled_job('cron', minute=dust_timer, name='get_air_quality') # '*/10', name = 'get_air_quality')
    def auto_mail():
        get_air_quality()

    hum_timer = ScheduleSettings.objects.get(type='humiditySensor')
    hum_timer = hum_timer.timer
    hum_timer = '*/' + hum_timer
    @scheduler.scheduled_job('cron', minute=hum_timer, name='get_humidity') # '*/10', name='get_humidity')
    def auto_humidity():
        get_humidity()

    scheduler.start()
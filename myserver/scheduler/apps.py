from django.apps import AppConfig
from django.conf import settings

class MailConfig(AppConfig):
    name = 'scheduler'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from scheduler import operator
            operator.start()
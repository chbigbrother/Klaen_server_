from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        task_list = Task.objects.all()

        for task in task_list:
            if task.end_date < datetime.now().date():
                task.state = 3
                task.save()
                print('ToDo :', task.name, '의 완료날짜(', task.end_date, ')가 지났습니다.')
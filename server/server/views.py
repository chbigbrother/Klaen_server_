from django.views.decorators.csrf import csrf_exempt
from background_task import background
from logging import getLogger
from django.http import JsonResponse
# forms.py
@csrf_exempt
def tasks(request):
     if request.method == 'POST':
         message = request.POST.get('message', False)
         print("kkkk")
         return demo_task(request)
     else:
        return JsonResponse({}, status=405)

logger = getLogger(__name__)

@background(schedule=10)
def demo_task(message):
    logger.debug('demo_task. message={0}'.format(message))
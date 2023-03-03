from .tasks import reservation_state_change
from background_task.models import Task

# 예약 상태 확인
class AirQualCheck(request):
    def get(self, request):
        reservation_state_change(repeat=Task.DAILY)
        return Response(status=status.HTTP_302_FOUND)
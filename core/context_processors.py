from django.utils import timezone
import pytz


def tz(request):
    return {
        'current_time': timezone.now(),
        'timezones': pytz.common_timezones,
    }

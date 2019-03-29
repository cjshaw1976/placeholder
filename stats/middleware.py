from django.db.models import F
from django.http import HttpResponse

from celery import shared_task
import datetime
import time

from .models import DataLog, GeoCities, GeoIP, LocationLog, VisitorLog

""" Callable current hour """
def currentHour():
    return datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)

""" IP Location lookup """
def getLocation(ipaddress):
    results = GeoIP.objects.extra(where=["INET_ATON('{}') BETWEEN INET_ATON(start_ip) AND INET_ATON(end_ip)".format(ipaddress)])
    if results:
        result = results[0]
        return result.geoname_id
    else:
        return None


""" Log where our placeholders are being used, count uses by hour """
@shared_task
class LogRequestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        "Start time at request coming in"
        request.start_time = time.time()

    def process_response(self, request, response):
        "End of request, take time"
        total = time.time() - request.start_time

        # Add the header.
        response["X-total-time"] = int(total * 1000)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # Try to get the referer
        referer=request.META.get('HTTP_REFERER')
        if referer == None:             # No referer, we assume it is ours
            secure = ''
            if request.is_secure:
                secure = 's'
            referer = ('http{}://{}').format(secure, request.META.get('HTTP_HOST'))

        # Try to get the client address
        remote=request.META.get('REMOTE_ADDR')
        if remote == None:
            remote = '0.0.0.0'

        location=getLocation(remote)

        # Get or create a new object URI hit
        obj, created = DataLog.objects.get_or_create(
            referer=referer,
            uri=request.META['REQUEST_URI'],
            hour=currentHour())
        obj.count = F('count') + 1      # Increment the count
        obj.save()

        # Get or create a new visitor hit
        results = VisitorLog.objects.filter(remote=remote,
            agent=request.META['HTTP_USER_AGENT'], location=location,
            date_added__gte=datetime.datetime.now() - datetime.timedelta(minutes=10))
        if results:
            result = results[0]
            result.count = result.count + 1
            result.save()
        else:
           result = VisitorLog.objects.create(remote=remote,
           agent=request.META['HTTP_USER_AGENT'], location=location, count=1)

        # Get or create a new location hit
        obj, created = LocationLog.objects.get_or_create(
            location=location,
            hour=currentHour())
        obj.count = F('count') + 1      # Increment the count
        obj.save()

        return None

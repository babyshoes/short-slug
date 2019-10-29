from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from .models import URL, Visit
from .helpers import encode, validate, recreate

def index(request):
    return HttpResponse(f"some info: {request.path} done")

def random(request, long_url):
    short_url = encode(long_url)
    return create_and_validate(long_url, short_url, custom=True)

def custom(request, long_url, short_url):
    return create_and_validate(long_url, short_url)

def create_and_validate(long_url, short_url, custom=False):
    try:
        validate(short_url)
        url = URL(
            short_url=short_url,
            long_url=long_url,
            create_time=timezone.now(),
            custom=custom
        )
        url.save()
        return HttpResponse(f"SAVED! {long_url} shortened to {short_url}")
    except ValueError as e:
        return HttpResponse(f"{e}")
    except IntegrityError as e:
        return HttpResponse(f"A slug by that name exists. {e}")
    except e:
        return HttpResponse(f"OOPSU {e}")

# make into own app
def reroute(request, slug):
    try:
        fwded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        ip_address = fwded_for.split(',')[-1].strip() if fwded_for else remote_addr

        url = URL.objects.get(short_url=slug)
        long_url = recreate(url.long_url)
        
        visit = Visit(
            url=url,
            visit_time=timezone.now(),
            user_ip=ip_address 
        )
        visit.save()
        return HttpResponse(f"{long_url}, {ip_address}, {remote_addr}")
        # return redirect(long_url)
    except URL.DoesNotExist:
        raise Http404("???")

def stats(request, slug):
    url = URL.objects.get(short_url=slug)
    visits = url.visit_set.count()
    data = {
        'short': url.short_url,
        'long': url.long_url,
        'create_time': url.create_time,
        'num_visits': visits,
    }
    return JsonResponse(data, safe=False)

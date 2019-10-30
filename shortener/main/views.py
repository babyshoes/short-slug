from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, Http404
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from .models import URL, Visit
from .forms import URLForm, CustomURLForm
from .helpers import encode, validate, recreate

def random(request):
    form = URLForm()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data.get("url")
            short_url = encode(long_url)
            return random_already_exists(long_url) or create_and_validate(long_url, short_url, custom=False)
    context = {'form': form}
    return render(request, 'main/random_url.html', context)

def custom(request):
    form = CustomURLForm()
    if request.method == "POST":
        form = CustomURLForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data.get("url")
            short_url = form.cleaned_data.get("short")
            return create_and_validate(long_url, short_url, custom=True)
    context = {'form': form}
    return render(request, 'main/custom_url.html', context)

def random_already_exists(long_url):
    try:
        exists = URL.objects.get(long_url=long_url, custom=False)
        return HttpResponse(f"{exists.long_url} already shortened to {exists.short_url}")
    except:
        return None

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
    except BaseException as e:
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

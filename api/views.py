from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone


def health(request):
    now = timezone.localtime(timezone.now())
    return JsonResponse({'date': now})


def unhealth(request):
    class UnhealthTestException(Exception):
        pass

    now = timezone.localtime(timezone.now())
    raise UnhealthTestException('/unhealth endpoint called on {}'.format(now))
    return 'It should have raised UnhealthTestException'

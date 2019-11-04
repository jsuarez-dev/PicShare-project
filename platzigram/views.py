"""
Platzigram views models
"""

# Django
from django.http import HttpResponse, JsonResponse
# Utilities
from datetime import datetime
import json


def hello_world(request):
    """Return and greeting"""
    now = datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
    return HttpResponse('Hi, the time in the server is {now}'.format(now=str(now)))


def sorted_numbers(request):
    """Return a JSON with sorted list of numbers"""
    numbers = request.GET['numbers']
    numbers_int = list(map(int, numbers.split(',')))
    numbers_int.sort()
    data = {
        'status': 'ok',
        'sorted numbers': numbers_int,
        'message': 'the numbers was sorted successfully'
    }
    return HttpResponse(json.dumps(data, indent=4), content_type='application/json')


def say_hi(request, name, age):
    """ Return a greeting"""
    if age <= 12:
        message = 'Sorry {name} you are not allow to use Platzigram'.format(name=name)
    else:
        message = 'Welcome to Platzigram {name}'.format(name=name)

    return HttpResponse(message)

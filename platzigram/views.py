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


def hi(request):
    """Sort Numbers"""
    numbers = request.GET['numbers']
    numbers_int = list(map(int, numbers.split(',')))
    numbers_int.sort()
    data = {
        'status': 'ok',
        'sorted numbers': numbers_int,
        'message': 'the numbers was sorted successfully'
    }
    return HttpResponse(json.dumps(data, indent=4), content_type='application/json')

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from shortener_url.models import Url
import hashlib
import time


@api_view(['POST'])
def create_shortener(request):
    
    try:
        url = request.data.get('url', False)
        if url:
            custom_alias = request.data.get('CUSTOM_ALIAS', False)
            
            if custom_alias and Url.objects.filter(custom_alias=custom_alias):
                return JsonResponse({'alias': custom_alias, 'err_code':'001', 'description': 'CUSTOM ALIAS ALREADY EXISTS'}, status=400)
            else:
                start = time.time()
                if custom_alias:
                    short_url = "http://shortener/u/{}".format( custom_alias )
                else:
                    custom_alias = hashlib.sha256( str( Url.objects.all().count() ).encode('utf-8') ).hexdigest()[:6] 
                    short_url = "http://shortener/u/{}".format( custom_alias )
                Url.objects.create(original_url=url, custom_alias=custom_alias, short_url=short_url)
                end = time.time()
                return JsonResponse({'url': short_url, 
                                    'alias': custom_alias, 
                                    'statistics': {"time_taken": "{} ms".format( end-start ) } }, status=200)
        else:
            return JsonResponse({'url': url, 'err_code':'003', 'description': 'URL isrequired'}, status=400)
    except:
        return JsonResponse({'Error':'Internal server error :('}, status=500)

from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseRedirect
from shortener_url.models import Url
import hashlib
import time

@api_view(['POST'])
def create_shortener(request):
    try:
        url = request.data.get('url', '').strip()
        if url:
            start = time.time()
            custom_alias = request.data.get('CUSTOM_ALIAS', '').strip()

            if custom_alias:
                if Url.objects.filter(custom_alias=custom_alias):
                    return JsonResponse({'alias': custom_alias, 'err_code':'001', 'description': 'CUSTOM ALIAS ALREADY EXISTS.'}, status=409)
                else:
                    shortened_url = "http://shortener/u/{}".format( custom_alias )
            else:
                custom_alias = hashlib.sha256( str( Url.objects.all().last()._id ).encode('utf-8') ).hexdigest()[:6] 
                shortened_url = "http://shortener/u/{}".format( custom_alias )
 
            Url.objects.create(original_url=url, custom_alias=custom_alias, shortened_url=shortened_url)
            end = time.time()
            return JsonResponse({'url': shortened_url, 'alias': custom_alias, 'statistics': {"time_taken": "{} ms".format( end-start ) } }, status=201)
        else:
            return JsonResponse({'url': url, 'err_code':'003', 'description': 'URL is required'}, status=400)
    except:
        return JsonResponse({'Error':'Internal server error :('}, status=500)


@api_view(['GET'])
def retrieve_url(request, custom_alias=None):
    try:
        if custom_alias:
            url = Url.objects.filter(custom_alias=custom_alias)
            if url:
                url[0].new_access
                return HttpResponseRedirect(redirect_to=url[0].original_url)
            else:
                return JsonResponse({'alias': custom_alias, 'err_code':'002', 'description': 'SHORTENED URL NOT FOUND.'}, status=404)
        else:
           return JsonResponse({'alias': custom_alias, 'err_code':'003', 'description': 'alias is required.'}, status=400) 
    except:
        return JsonResponse({'Error':'Internal server error :('}, status=500)


@api_view(['GET'])
def top_urls_visited(request):
    try:
        urls = Url.objects.filter(accesses__gte=1).order_by('-accesses')[:10]
        if urls:
            data = list( urls.values('original_url', 'shortened_url', 'custom_alias', 'accesses') ) 
            return JsonResponse(data, safe=False, status=200)
        else:
           return JsonResponse({}, status=204) 
    except:
        return JsonResponse({'Error':'Internal server error :('}, status=500)


@api_view(['GET'])
def urls(request):
    try:
        urls = Url.objects.all()
        if urls:
            data = list( urls.values('original_url', 'shortened_url', 'custom_alias', 'accesses') ) 
            return JsonResponse(data, safe=False, status=200)
        else:
           return JsonResponse({}, status=204) 
    except:
        return JsonResponse({'Error':'Internal server error :('}, status=500)
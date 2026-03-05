from django.http import JsonResponse
from django.conf import settings
import requests

def proxy_request(service_url, request):
    try:
        url = f"{service_url}{request.path.replace('/api', '')}"
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers.items() if key != 'Host'},
            data=request.body,
            timeout=5
        )
        return JsonResponse(response.json(), status=response.status_code, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def proxy_user_service(request):
    return proxy_request(settings.SERVICES['user'], request)

def proxy_product_service(request):
    return proxy_request(settings.SERVICES['product'], request)

def proxy_order_service(request):
    return proxy_request(settings.SERVICES['order'], request)

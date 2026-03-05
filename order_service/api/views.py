from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

orders = [
    {'id': 1, 'userId': 1, 'productId': 1, 'quantity': 1, 'status': 'completed'},
    {'id': 2, 'userId': 2, 'productId': 2, 'quantity': 2, 'status': 'pending'}
]

@csrf_exempt
def orders_list(request):
    if request.method == 'GET':
        return JsonResponse(orders, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_order = {'id': len(orders) + 1, 'status': 'pending', **data}
        orders.append(new_order)
        return JsonResponse(new_order)

def order_detail(request, order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return JsonResponse(order)
    return JsonResponse({'error': 'Order not found'}, status=404)

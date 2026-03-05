from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

products = [
    {'id': 1, 'name': 'Laptop', 'price': 999, 'stock': 10},
    {'id': 2, 'name': 'Phone', 'price': 699, 'stock': 25},
    {'id': 3, 'name': 'Tablet', 'price': 499, 'stock': 15}
]

@csrf_exempt
def products_list(request):
    if request.method == 'GET':
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_product = {'id': len(products) + 1, **data}
        products.append(new_product)
        return JsonResponse(new_product)

def product_detail(request, product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return JsonResponse(product)
    return JsonResponse({'error': 'Product not found'}, status=404)

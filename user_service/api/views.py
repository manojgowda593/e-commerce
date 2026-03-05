from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

@csrf_exempt
def users_list(request):
    if request.method == 'GET':
        return JsonResponse(users, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_user = {'id': len(users) + 1, **data}
        users.append(new_user)
        return JsonResponse(new_user)

def user_detail(request, user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return JsonResponse(user)
    return JsonResponse({'error': 'User not found'}, status=404)

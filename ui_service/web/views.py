from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'users.html')

def products(request):
    return render(request, 'products.html')

def orders(request):
    return render(request, 'orders.html')

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'topfragmarket/pages/index.html')

def login(request):
    return render(request, 'topfragmarket/pages/login.html')

def categories(request):
    return render(request, 'topfragmarket/pages/categories.html')

def listings(request):
    return render(request, 'topfragmarket/pages/listings.html')
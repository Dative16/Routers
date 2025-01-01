from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'service/index.html')


def choose_location(request):
    return render(request, 'service/locations.html')

def payment_processing(request):
    return render(request, 'service/payment_page.html')

def user_payment_history(request):
    return render(request, 'service/user_payment_history.html')
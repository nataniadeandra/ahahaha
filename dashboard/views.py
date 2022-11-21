from django.shortcuts import render

# Create your views here.
def dashboard_pelanggan(request):
    return render(request, 'dashboard_pelanggan.html')

def dashboard_restoran(request):
    return render(request, 'dashboard_restoran.html')

def dashboard_kurir(request):
    return render(request, 'dashboard_kurir.html')
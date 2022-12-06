from django.shortcuts import render

# Create your views here.
def dashboard_pelanggan(request, pk):
    return render(request, 'dashboard_pelanggan.html')

def dashboard_restoran(request, pk):
    return render(request, 'dashboard_restoran.html')

def dashboard_kurir(request, pk):
    return render(request, 'dashboard_kurir.html')

def dashboard_admin(request, pk):
    return render(request, 'dashboard_admin.html')
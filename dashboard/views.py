from django.shortcuts import render

# Create your views here.
def dashboard_pelanggan(request, pk):
    return render(request, 'dashboard_pelanggan.html')

def dashboard_restoran(request, pk):
    return render(request, 'dashboard_restoran.html')

def dashboard_kurir(request, pk):
    return render(request, 'dashboard_kurir.html')

def detail_pelanggan(request, pk):
    return render(request, 'detail_pelanggan.html')

def detail_restoran(request, pk):
    return render(request, 'detail_restoran.html')

def detail_kurir(request, pk):
    return render(request, 'detail_kurir.html')
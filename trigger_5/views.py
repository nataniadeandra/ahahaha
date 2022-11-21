from django.shortcuts import render
from .forms import bahanMakananForm, kategoriRestoranForm
# Create your views here.
def show_bahan_makanan(request):
    
    return render(request, 'bahan_makanan.html')

def create_bahan_makanan(request):
    form_gen = bahanMakananForm()
    context = {
        'form' : form_gen
    }
    return render(request, 'bahan_makanan_create.html', context)

def show_kategori_restoran(request):
    return render(request, 'kategori_restoran.html')

def create_kategori_restoran(request):
    form_gen = kategoriRestoranForm()
    context = {
        'form' : form_gen
    }
    return render(request, 'kategori_restoran_create.html', context)

def show_transaksi_pesanan_kurir(request):
    return render(request, 'transaksi_pesanan_kurir.html')

def show_transaksi_pesanan_kurir_detail(request):
    return render(request, 'transaksi_pesanan_kurir_detail.html')
from django.shortcuts import render
from .forms import kategoriMakananForm, pengisianAlamatPesananMakananForm

# Create your views here.

# CR Kategori Makanan
def create_kategori_makanan(request):
    form = kategoriMakananForm()
    if request.method == "POST":
        form = kategoriMakananForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'kategori_makanan_form.html', context)

def read_kategori_makanan(request):
    return render(request, 'kategori_makanan_list.html')

def create_alamat_pesanan(request):
    form = pengisianAlamatPesananMakananForm()
    if request.method == "POST":
        form = pengisianAlamatPesananMakananForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'alamat_pesanan_form.html', context)

def konfirmasi_pembayaran(request):
    return render(request, 'konfirmasi_pembayaran.html')

def pemilihan_detail_pesanan(request):
    return render(request, 'pemilihan_detail_pesana.html')

def pemilihan_restoran(request):
    return render(request, 'pemilihan_restoran.html')

def pesanan_berlangsung(request):
    return render(request, 'pesanan_berlangsung.html')

def ringkasan_pesanan(request):
    return render(request, 'ringkasan_pesanan.html')

def daftar_pesanan(request):
    return render(request, 'daftar_pesanan.html')
from django.shortcuts import render
from .forms import bahanMakananForm, kategoriRestoranForm
from util.query import query
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
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
    data = {}
    list_kategori_restoran = query(f"""
    SELECT Id, Name
    FROM RESTAURANT_CATEGORY
    """)
    data['item_list'] = list_kategori_restoran
    # print(data['item_list'])
    return render(request, 'kategori_restoran.html', data)

def create_kategori_restoran(request):
    form_gen = kategoriRestoranForm()
    context = {
        'form' : form_gen
    }
    return render(request, 'kategori_restoran_create.html', context)

def delete_kategori_restoran(request, id):
    print(id)
    query(f"""
    DELETE FROM RESTAURANT_CATEGORY
    WHERE Id = '{id}'
    """)
    response = HttpResponseRedirect(reverse("trigger_5:show_kategori_restoran"))
    return response

def show_transaksi_pesanan_kurir(request):
    return render(request, 'transaksi_pesanan_kurir.html')

def show_transaksi_pesanan_kurir_detail(request):
    return render(request, 'transaksi_pesanan_kurir_detail.html')
from django.shortcuts import render
from sirest.utils import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from sirest.utils import get_role, is_authenticated
from django.db import connection

# Create your views here.
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def tambah_makanan(request):
    return render(request, 'makanan_add.html')

def update_makanan(request):
    return render(request, 'makanan_update.html')

def makanan_page(request):
    # if is_authenticated(request) == True:
    #     cursor = connection.cursor()
    #     cursor.execute()
    # else:
    #     response = HttpResponseRedirect(reverse("login_page:login"))
    #     return response
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO SIREST")
    cursor.execute('SELECT * FROM FOOD INNER JOIN FOOD_CATEGORY ON FOOD.FCATEGORY = FOOD_CATEGORY.id')
    hasil = namedtuplefetchall(cursor)
    print (hasil)
    return render(request, 'makanan.html', {'hasil':hasil})

def restoran_detail_makanan(request):
    return render(request, 'restoran_makanan_detail.html')

def restoran_menu_makanan(request):
    return render(request, 'restoran_makanan_menu.html')

def restoran_makanan_page(request):
    return render(request, 'restoran_makanan.html')

def tarif_pengiriman_page(request):
    return render(request, 'tarif_pengiriman.html')

def tambah_tarif_pengiriman(request):
    return render(request, 'tarif_pengiriman_add.html')

def update_tarif_pengiriman(request):
    return render(request, 'tarif_pengiriman_update.html')
from django.shortcuts import render, redirect
from sirest.utils import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from sirest.utils import get_role, is_authenticated
from django.db import connection
from django.urls import reverse

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
    return render(request, 'makanan.html', {'hasil':hasil})

def delete_makanan(request, rname, rbranch, foodname): 
    get_query(f"""
        DELETE FROM sirest.FOOD 
        WHERE rname = '{rname}' AND rbranch = '{rbranch}' AND foodname = '{foodname}';
    """)
    return redirect('/trigger_3/makanan/')

def restoran_detail_makanan(request):
    return render(request, 'restoran_makanan_detail.html')

def restoran_menu_makanan(request):
    return render(request, 'restoran_makanan_menu.html')

def restoran_makanan_page(request):
    return render(request, 'restoran_makanan.html')

def tarif_pengiriman_page(request):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO SIREST")
    cursor.execute('SELECT * FROM DELIVERY_FEE_PER_KM')
    hasil = namedtuplefetchall(cursor)
    return render(request, 'tarif_pengiriman.html', {'hasil':hasil})

def tambah_tarif_pengiriman(request):
    return render(request, 'tarif_pengiriman_add.html')

def update_tarif_pengiriman(request):
    return render(request, 'tarif_pengiriman_update.html')

def delete_tarif_pengiriman(request, id): 
    get_query(f"""
        DELETE FROM sirest.DELIVERY_FEE_PER_KM 
        WHERE id = '{id}';  
    """)

    return redirect('/trigger_3/tarif_pengiriman/')
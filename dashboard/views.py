from django.shortcuts import render
from sirest.utils import *

# Create your views here.
def dashboard_pelanggan(request):
    email_pelanggan = str(request.session["email"])
    pelanggan = get_query(
        f'''
        SELECT *
        FROM sirest.user_acc
        NATURAL JOIN sirest.transaction_actor
        NATURAL JOIN sirest.customer
        WHERE email='{email_pelanggan}';
        '''
    )[0]

    if pelanggan[9] == None or pelanggan[9] == "None":
        status = "Belum terferivikasi"
        nama_admin = ""
        terverifikasi = False
    else:
        status = "Terverifikasi"
        query_admin = get_query(
            f'''
            SELECT fname, lname
            FROM sirest.user_acc
            WHERE email = '{pelanggan[9]}'
            '''
        )[0]
        nama_admin = query_admin[0] + " " + query_admin[1]
        terverifikasi = True

    context = {
        "email" : pelanggan[0],
        "password" : pelanggan[1],
        "nama" : pelanggan[3] + " " + pelanggan[4],
        "nomor_hp" : pelanggan[2],
        "nik" : pelanggan[5],
        "nama_bank" : pelanggan[6],
        "nomor_rekening" : pelanggan[7],
        "tanggal_lahir" : pelanggan[10],
        "jenis_kelamin" : pelanggan[11],
        "status" : status,
        "diverifikasi_oleh" : nama_admin,
        "terverifikasi" : terverifikasi,
        "saldo_restopay" : pelanggan[8]
    }

    return render(request, 'dashboard_pelanggan.html', context)

def dashboard_restoran(request):
    email_restoran = str(request.session["email"])
    restoran  = get_query(
        f'''
        SELECT *
        FROM sirest.user_acc
        NATURAL JOIN sirest.transaction_actor
        NATURAL JOIN sirest.restaurant
        WHERE email='{email_restoran}';
        '''
    )[0]

    kategori_restoran = get_query(
        f'''
        SELECT name
        FROM sirest.restaurant_category
        WHERE id = '{restoran[18]}';
        '''
    )[0][0]

    jam_operasional = get_query(
        f'''
        SELECT *
        FROM sirest.restaurant_operating_hours
        WHERE name = '{restoran[10]}' AND branch = '{restoran[11]}';
        '''
    )

    if restoran[9] == None or restoran[9] == "None":
        status = "Belum terferivikasi"
        nama_admin = ""
        terverifikasi = False
    else:
        status = "Terverifikasi"
        query_admin = get_query(
            f'''
            SELECT fname, lname
            FROM sirest.user_acc
            WHERE email = '{restoran[9]}'
            '''
        )[0]
        nama_admin = query_admin[0] + " " + query_admin[1]
        terverifikasi = True

    # email password phonenum fname lname nik bankname accountno restopay 9 addminid rname rbranch rphonenum street district city province rating rcategory
    
    context = {
        "email" : restoran[0],
        "password" : restoran[1],
        "nama" : restoran[3] + " " + restoran[4],
        "nomor_hp" : restoran[2],
        "nik" : restoran[5],
        "nama_bank" : restoran[6],
        "nomor_rekening" : restoran[7],
        "nama_restoran" : restoran[10],
        "cabang" : restoran[11],
        "nomor_telepon" : restoran[12],
        "jalan" : restoran[13],
        "kecamatan" : restoran[14],
        "kota" : restoran[15],
        "provinsi" : restoran[16],
        "rating" : restoran[17],
        "kategori_restoran" : kategori_restoran,
        "jam_operasional" : jam_operasional,
        "status" : status,
        "diverifikasi_oleh" : nama_admin,
        "terverifikasi" : terverifikasi,
        "saldo_restopay" : restoran[8]
    }
    return render(request, 'dashboard_restoran.html', context)

def dashboard_kurir(request):
    return render(request, 'dashboard_kurir.html')

def dashboard_admin(request, pk):
    return render(request, 'dashboard_admin.html')

def detail_pelanggan(request):
    return render(request, 'detail_pelanggan.html')

def detail_restoran(request):
    return render(request, 'detail_restoran.html')

def detail_kurir(request):
    return render(request, 'detail_kurir.html')
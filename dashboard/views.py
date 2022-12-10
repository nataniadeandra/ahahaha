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
    email_kurir = str(request.session["email"])

    kurir = get_query(
        f'''
        SELECT *
        FROM sirest.user_acc
        NATURAL JOIN sirest.transaction_actor
        NATURAL JOIN sirest.courier
        WHERE email='{email_kurir}'
        '''
    )[0]

    if kurir[9] == None or kurir[9] == "None":
        status = "Belum terferivikasi"
        nama_admin = ""
        terverifikasi = False
    else:
        status = "Terverifikasi"
        query_admin = get_query(
            f'''
            SELECT fname, lname
            FROM sirest.user_acc
            WHERE email = '{kurir[9]}'
            '''
        )[0]
        nama_admin = query_admin[0] + " " + query_admin[1]
        terverifikasi = True

    context = {
        "email" : kurir[0],
        "password" : kurir[1],
        "nama" : kurir[3] + " " + kurir[4],
        "nomor_hp" : kurir[2],
        "nik" : kurir[5],
        "nama_bank" : kurir[6],
        "nomor_rekening" : kurir[7],
        "plat_nomor_kendaraan" : kurir[10],
        "nomor_sim" : kurir[11],
        "jenis_kendaraan" : kurir[12],
        "merk_kendaraan" : kurir[13],
        "status" : status,
        "diverifikasi_oleh" : nama_admin,
        "terverifikasi" : terverifikasi,
        "saldo_restopay" : kurir[8]
    }

    return render(request, 'dashboard_kurir.html', context)

def dashboard_admin(request):
    email_admin = str(request.session["email"])
    admin  = get_query(
        f'''
        SELECT *
        FROM sirest.user_acc
        NATURAL JOIN sirest.admin
        WHERE email='{email_admin}';
        '''
    )[0]

    tabel_pengguna = get_query(
        f'''
        SELECT ua.email, ua.fname, ua.lname, COUNT(cu.email) as pelanggan, COUNT(r.email) as restoran, COUNT(co.email) as kurir, COUNT(ta.adminid) as terverifikasi
        FROM sirest.user_acc ua
        NATURAL JOIN sirest.transaction_actor ta
        LEFT OUTER JOIN sirest.customer cu
        ON ua.email = cu.email
        LEFT OUTER JOIN sirest.restaurant r
        ON ua.email = r.email
        LEFT OUTER JOIN sirest.courier co
        ON ua.email = co.email
        GROUP BY ua.email,ua.fname, ua.lname, ta.adminid;
        '''
    )

    context = {
        "email" : admin[0],
        "password" : admin[1],
        "nama" : admin[3] + " " + admin[4],
        "nomor_hp" : admin[2],
        "pengguna" : tabel_pengguna,
    }

    return render(request, 'dashboard_admin.html', context)

def detail_pelanggan(request, email):
    email_pelanggan = email
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

    return render(request, 'detail_pelanggan.html', context)

def detail_restoran(request, email):

    email_restoran = email
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

    promo = get_query(
        f'''
        SELECT p.promoname
        FROM sirest.promo p
        INNER JOIN sirest.restaurant_promo rp
        ON p.id = rp.pid
        INNER JOIN sirest.restaurant r
        ON rp.rname = r.rname and rp.rbranch = r.rbranch
        WHERE r.email = '{email}';
        '''
    )
    
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
        "promo" : promo,
        "status" : status,
        "diverifikasi_oleh" : nama_admin,
        "terverifikasi" : terverifikasi,
        "saldo_restopay" : restoran[8]
    }

    return render(request, 'detail_restoran.html', context)

def detail_kurir(request, email):
    email_kurir = email

    kurir = get_query(
        f'''
        SELECT *
        FROM sirest.user_acc
        NATURAL JOIN sirest.transaction_actor
        NATURAL JOIN sirest.courier
        WHERE email='{email_kurir}'
        '''
    )[0]

    if kurir[9] == None or kurir[9] == "None":
        status = "Belum terferivikasi"
        nama_admin = ""
        terverifikasi = False
    else:
        status = "Terverifikasi"
        query_admin = get_query(
            f'''
            SELECT fname, lname
            FROM sirest.user_acc
            WHERE email = '{kurir[9]}'
            '''
        )[0]
        nama_admin = query_admin[0] + " " + query_admin[1]
        terverifikasi = True

    context = {
        "email" : kurir[0],
        "password" : kurir[1],
        "nama" : kurir[3] + " " + kurir[4],
        "nomor_hp" : kurir[2],
        "nik" : kurir[5],
        "nama_bank" : kurir[6],
        "nomor_rekening" : kurir[7],
        "plat_nomor_kendaraan" : kurir[10],
        "nomor_sim" : kurir[11],
        "jenis_kendaraan" : kurir[12],
        "merk_kendaraan" : kurir[13],
        "status" : status,
        "diverifikasi_oleh" : nama_admin,
        "terverifikasi" : terverifikasi,
        "saldo_restopay" : kurir[8]
    }

    return render(request, 'detail_kurir.html', context)
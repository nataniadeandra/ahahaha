from django.shortcuts import redirect, render
from sirest.utils import *

# Create your views here.
def read_resto_pay(request):
    email = str(request.session["email"])
    role = str(request.session["role"])

    query = get_query(
        f'''
        SELECT restopay
        FROM sirest.transaction_actor
        WHERE email = '{email}'
        '''
    )[0]

    return render(request, 'read_resto_pay.html', {"query" : query, "role" : role})

def isi_resto_pay(request):
    
    email = str(request.session["email"])
    role = str(request.session["role"])

    query = get_query(
        f'''
        SELECT restopay, bankname, accountno
        FROM sirest.transaction_actor
        WHERE email = '{email}'
        '''
    )[0]

    if request.method != "POST":
        return render(request, 'isi_resto_pay.html', {"query" : query, "role" : role})

    isi = int(request.POST["isi"])

    get_query(
        f'''
        UPDATE sirest.transaction_actor
        SET restopay = restopay + {isi}
        WHERE email='{email}';
        '''
    )

    return render(request, 'isi_resto_pay.html', {"query" : query, "role" : role})

def tarik_resto_pay(request):
    
    email = str(request.session["email"])
    role = str(request.session["role"])

    query = get_query(
        f'''
        SELECT restopay, bankname, accountno
        FROM sirest.transaction_actor
        WHERE email = '{email}'
        '''
    )[0]

    if request.method != "POST":
        return render(request, 'tarik_resto_pay.html', {"query" : query, "role" : role})

    tarik = int(request.POST["tarik"])

    result = get_query(
        f'''
        UPDATE sirest.transaction_actor
        SET restopay = restopay - {tarik}
        WHERE email='{email}';
        '''
    )

    if str(result).strip() == "'NoneType' object is not iterable":
        return render(request, 'tarik_resto_pay.html', {"query" : query, "role" : role})
    else:
        return render(request, 'tarik_resto_pay.html', {"query" : query, "message" : str(result).split("CONTEXT")[0], "role" : role})

def read_transaksi_pesanan_restoran(request):

    email = str(request.session["email"])

    query = get_query(
        f'''
        SELECT distinct uac.fname as fname, uac.lname as lname, uac.email as email, tf.datetime as datetime, ts.name as status, ts.id as status_id
        FROM sirest.transaction_food tf
        INNER JOIN sirest.restaurant r ON tf.rname = r.rname and tf.rbranch = r.rbranch
        INNER JOIN sirest.user_acc uar ON r.email = uar.email
        INNER JOIN sirest.user_acc uac ON tf.email = uac.email
        INNER JOIN sirest.transaction t ON tf.email = t.email and tf.datetime = t.datetime
        INNER JOIN sirest.transaction_history th ON t.email = th.email and t.datetime = th.datetime
        INNER JOIN sirest.transaction_status ts ON th.tsid = ts.id
        WHERE uar.email = '{email}';
        '''
    )

    datetime = str(query[0].datetime)[:23]

    return render(request, 'transaksi_pesanan_restoran.html', {"query" : query, "datetime" : datetime})

def update_transaksi_pesanan_restoran(request, email, datetime):

    get_query(
        f'''
        UPDATE sirest.transaction_history
        SET tsid = 'TS02'
        WHERE email = '{email}' and datetime = '{datetime}' and tsid = 'TS01';
        '''
    )

    get_query(
        f'''
        UPDATE sirest.transaction_history
        SET tsid = 'TS03'
        WHERE email = '{email}' and datetime = '{datetime}' and tsid = 'TS02';
        '''
    )

    return redirect("../../../read/")

def detail_transaksi_pesanan_restoran(request, email, datetime):

    nama_pelanggan = get_query(
        f'''
        SELECT fname, lname
        FROM sirest.user_acc
        WHERE email = '{email}';
        '''
    )[0]

    alamat_pelanggan = get_query(
        f'''
        SELECT street, district, city, province
        FROM sirest.transaction t
        WHERE email = '{email}' and datetime = '{datetime}';
        '''
    )[0]

    alamat_restoran = get_query(
        f'''
        SELECT rname, rbranch, street, district, city, province
        FROM sirest.restaurant
        WHERE email = '{request.session["email"]}';
        '''
    )[0]

    makanan = get_query(
        f'''
        SELECT foodname, amount, note
        FROM sirest.transaction_food
        WHERE email = '{email}' and datetime = '{datetime}' and rname = '{alamat_restoran[0]}' and rbranch = '{alamat_restoran[1]}';
        '''
    )

    pengantaran = get_query(
        f'''
        SELECT t.totalfood, t.totaldiscount, t.deliveryfee, t.totalprice, t.pmid, pm.name
        FROM sirest.transaction as t
        INNER JOIN sirest.payment_method as pm ON t.pmid = pm.id 
        WHERE t.email = '{email}' and t.datetime = '{datetime}';
        '''
    )[0]

    # BELOM
    context = {
        "datetime" : datetime,
        "nama_pelanggan" : nama_pelanggan[0] + " " + nama_pelanggan[1],
        "jalan_pelanggan" : alamat_pelanggan[0],
        "kecamatan_pelanggan" : alamat_pelanggan[1],
        "kota_pelanggan" : alamat_pelanggan[2],
        "provinsi_pelanggan" : alamat_pelanggan[3],
        "nama_restoran" : alamat_restoran[0],
        "jalan_restoran" : alamat_restoran[2],
        "kecamatan_restoran" : alamat_restoran[3],
        "kota_restoran" : alamat_restoran[4],
        "provinsi_restoran" : alamat_restoran[5],
        "makanan" : makanan,
        "total_harga_makanan" : pengantaran[0],
        "total_diskon" : pengantaran[1],
        "biaya_pengantaran" : pengantaran[2],
        "total_biaya" : pengantaran[3],
        "jenis_pembayaran" : pengantaran[4]

    }

    return render(request, 'detail_transaksi_pesanan_restoran.html', context)

def create_jam_operasional(request):

    email = str(request.session["email"])

    if request.method != "POST":
        return render(request, 'create_jam_operasional.html')

    query = get_query(
        f'''
        SELECT rname, rbranch
        FROM sirest.restaurant
        WHERE email = '{email}'
        '''
    )[0]

    rname = query[0]
    rbranch = query[1]

    hari = request.POST["hari"]
    jam_buka = request.POST["jam-buka"]
    jam_tutup = request.POST["jam-tutup"]

    get_query(
        f'''
        INSERT INTO sirest.restaurant_operating_hours
        VALUES ('{rname}', '{rbranch}', '{hari}', '{jam_buka}', '{jam_tutup}');
        '''
    )

    return redirect("../read/")

def read_jam_operasional(request):

    email = str(request.session["email"])

    query  = get_query(
        f'''
        SELECT roh.day as day, roh.starthours as starthours, roh.endhours as endhours, r.email
        FROM sirest.restaurant_operating_hours roh
        INNER JOIN sirest.restaurant r
        ON roh.name = r.rname and roh.branch = r.rbranch
        WHERE r.email = '{email}';
        '''
    )
    return render(request, 'read_jam_operasional.html', {"query" : query})

def update_jam_operasional(request, day):

    email = str(request.session["email"])

    if request.method != "POST":
        return render(request, 'update_jam_operasional.html', {"day" : day})

    query = get_query(
        f'''
        SELECT rname, rbranch
        FROM sirest.restaurant
        WHERE email = '{email}'
        '''
    )[0]

    rname = query[0]
    rbranch = query[1]

    jam_buka = request.POST["jam-buka"]
    jam_tutup = request.POST["jam-tutup"]

    get_query(
        f'''
        UPDATE sirest.restaurant_operating_hours
        SET starthours = '{jam_buka}', endhours = '{jam_tutup}'
        WHERE name = '{rname}' AND branch = '{rbranch}' AND day = '{day}';
        '''
    )

    return redirect("../../read/")

def delete_jam_operasional(request, day):

    email = str(request.session["email"])

    query = get_query(
        f'''
        SELECT rname, rbranch
        FROM sirest.restaurant
        WHERE email = '{email}'
        '''
    )[0]

    rname = query[0]
    rbranch = query[1]

    get_query(
        f'''
        DELETE FROM sirest.restaurant_operating_hours
        WHERE name = '{rname}' AND branch = '{rbranch}' AND day = '{day}';
        '''
    )

    return redirect('../../read/')
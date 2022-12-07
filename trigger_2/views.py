from django.shortcuts import redirect, render
from sirest.utils import *

from datetime import datetime as dt

# Create your views here.
def read_resto_pay(request):
    email = str(request.session["email"]).strip()
    role = str(request.session["role"]).strip()

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
    
    email = str(request.session["email"]).strip()
    role = str(request.session["role"]).strip()

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

    email = str(request.session["email"]).strip()

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
        WHERE uar.email = '{email}' and (ts.id = 'TS01' or ts.id = 'TS02' or ts.id = 'TS03')
        ORDER BY ts.id DESC
        LIMIT 1;
        '''
    )

    if (len(query) == 0):
        return render(request, 'transaksi_pesanan_restoran.html', {"query" : query})
    else:
        return render(request, 'transaksi_pesanan_restoran.html', {"query" : query, "datetime" : str(query[0].datetime)[:23]})

def update_transaksi_pesanan_restoran(request, email, datetime, status_id):

    if (status_id == 'TS01'):
        new_status_id = 'TS02'
    elif (status_id == 'TS02'):
        new_status_id = 'TS03'

    current_date = str(dt.now())[:23]

    get_query(
        f'''
        INSERT INTO sirest.transaction_history
        VALUES ('{email}', '{datetime}', '{new_status_id}', '{current_date}')
        '''
    )

    return redirect("../../../../read/")

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
        SELECT t.totalfood, t.totaldiscount, t.deliveryfee, t.totalprice, pm.name, t.psid
        FROM sirest.transaction t
        INNER JOIN sirest.payment_method as pm ON t.pmid = pm.id 
        WHERE t.email = '{email}' and t.datetime = '{datetime}';
        '''
    )[0]

    pembayaran = get_query(
        f'''
        SELECT name
        FROM sirest.payment_status
        WHERE id = '{pengantaran[5]}';
        '''
    )[0][0]

    query_status_pesanan = get_query(
        f'''
        SELECT ts.name, ts.id
        FROM sirest.transaction_history th
        INNER JOIN sirest.transaction_status ts
        ON th.tsid = ts.id
        WHERE email = '{email}' and datetime = '{datetime}'
        ORDER BY th.tsid DESC
        LIMIT 1;
        '''
    )[0]

    print(query_status_pesanan[0])
    print(query_status_pesanan[1])

    status_pesanan = query_status_pesanan[0]
    id_status_pesanan = query_status_pesanan[1]

    if id_status_pesanan == 'TS01' or id_status_pesanan == 'TS02':
        kurir = '-'
        plat_kendaraan = '-'
        jenis_kendaraan = '-'
        merk_kendaraan = '-'
    else:
        query_kurir = get_query(
            f'''
            SELECT ua.fname as fname, ua.lname as lname, c.platenum as platenum, c.vehicletype as vtype, c.vehiclebrand as branch
            FROM sirest.user_acc ua
            INNER JOIN sirest.courier c
            ON ua.email = c.email
            INNER JOIN sirest.transaction t
            ON t.courierid = c.email
            WHERE t.email = '{email}' and t.datetime = '{datetime}';
            '''
        )[0]

        kurir = query_kurir[0] + " " + query_kurir[1]
        plat_kendaraan = query_kurir[2]
        jenis_kendaraan = query_kurir[3]
        merk_kendaraan = query_kurir[4]

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
        "jenis_pembayaran" : pengantaran[4],
        "status_pembayaran" : pembayaran,
        "status_pesanan" : status_pesanan,
        "kurir" : kurir,
        "plat_kendaraan" : plat_kendaraan,
        "jenis_kendaraan" : jenis_kendaraan,
        "merk_kendaraan" : merk_kendaraan,
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
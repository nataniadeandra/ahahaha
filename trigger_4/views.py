from json import tool
from django.shortcuts import render, redirect
from django.contrib import messages
from util.query import *
from datetime import datetime as date


from login_page.views import get_session_data

# Create your views here.

# CR Kategori Makanan
def create_kategori_makanan(request):

    if request.method != "POST":
        return render(request, 'kategori_makanan_form.html')
    
    nama_kategori = request.POST['name']
    id_kategori = ""

    # Menentukan ID
    max_id_get = query("SELECT MAX(id) FROM food_category;")
    max_id = max_id_get[0][0][-2:]
    id_kategori = "FC" + str(int(max_id) + 1).zfill(2);

    query(
        f"""
        INSERT INTO food_category VALUES ('{id_kategori}', '{nama_kategori}');
    """)

    return redirect('/trigger-4/list-kategori-makanan/')
    

def delete_kategori_makanan(request, id): 
    query(f"""
        DELETE FROM food_category 
        WHERE id = '{id}';
    """)

    return redirect('/trigger-4/list-kategori-makanan/')

def read_kategori_makanan(request):
    data = get_session_data(request)

    data['kategori_makanan'] = query("""
        SELECT * FROM food_category;
    """)

    return render(request, 'kategori_makanan_list.html', data)

# CR Transaksi Pelanggan Alamat
def create_alamat_pesanan(request):
    data = get_session_data(request)

    province_list = query("""
        SELECT province FROM delivery_fee_per_km;
    """)
    data['province_list'] = province_list

    if request.method != "POST":
        return render(request, 'tpel_alamat_form.html', data)

    street = request.POST['street']
    district = request.POST['district']
    city = request.POST['city']
    province = request.POST['province']

    response = redirect('/trigger-4/list-resto/' + province + '/')

    response.set_cookie('street', street)
    response.set_cookie('district', district)
    response.set_cookie('city', city)
    response.set_cookie('province', province)
    return response


def pilih_restolist_pesanan(request, province):
    data = get_session_data(request)

    restaurant_list = query(f"""
        SELECT rname, rbranch
        FROM restaurant
        WHERE province = '{province}';
    """)
    promo_list = query(f"""
        SELECT rp.rname, rp.rbranch, p.promoname
        FROM restaurant_promo rp 
            INNER JOIN promo p ON rp.pid = p.id
    """)
    data['restaurant_list'] = restaurant_list
    data['promo_list'] = promo_list

    return render(request, 'tpel_choose_restolist_form.html', data)


def pilih_restomenu_pesanan(request, rname, rbranch):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()
    current_date = str(date.now())[:23]
    
    menu_list = query(f"""
        SELECT foodname, price
        FROM food
        WHERE rname = '{rname}' AND rbranch = '{rbranch}';
    """)
    payment_list = query(f"""
        SELECT name
        FROM payment_method;
    """)

    data['menu_list'] = menu_list
    data['payment_list'] = payment_list
    menu_count = len(menu_list)

    if request.method != "POST":
        return render(request, 'tpel_choose_restomenu_form.html', data)

    # AFTER POST
    vehicle = request.POST['vehicle']
    payment = request.POST['payment']

    street = request.COOKIES.get('street')
    district = request.COOKIES.get('district')
    city = request.COOKIES.get('city')
    province = request.COOKIES.get('province')
    
    total_food = 0
    amount_food = 0

    for i in range(menu_count):
        menu_qty = int(request.POST['jumlah-' + str(i+1)])
        if menu_qty > 0:
            amount_food += menu_qty
            total_food += menu_qty * menu_list[i][1]
        else:
            continue
    
    if amount_food == 0:
        messages.warning(request, "Silahkan pilih menu terlebih dahulu!")
        return redirect('/trigger-4/list-menu/' + rname + '/' + rbranch + '/')

    diskon_mt = query(f"""
        SELECT SUM(p.discount)
        FROM restaurant_promo rp INNER JOIN promo p on rp.pid = p.id INNER JOIN min_transaction_promo mtp on p.id = mtp.id
        WHERE rname = '{rname}' AND rbranch = '{rbranch}' AND mtp.minimumtransactionnum <= {total_food};
    """)

    diskon_sp = query(f"""
        SELECT SUM(p.discount)
        FROM restaurant_promo rp INNER JOIN promo p on rp.pid = p.id INNER JOIN special_day_promo sdp on p.id = sdp.id
        WHERE rname = '{rname}' AND rbranch = '{rbranch}';
    """)


    if diskon_mt[0][0] == None and diskon_sp[0][0] == None:
        total_diskon = 0
    elif diskon_mt[0][0] == None:
        total_diskon = int(diskon_sp[0][0])
    elif diskon_sp[0][0] == None:
        total_diskon = int(diskon_mt[0][0])
    else:
        total_diskon = int(diskon_mt[0][0]) + int(diskon_sp[0][0])

    diskon_value = total_food * total_diskon / 100

    pmid = ""
    if payment == "RestoPay":
        pmid = "PM01"
    elif payment == "Other e-Wallet":
        pmid = "PM02"
    elif payment == "Bank Transfer":
        pmid = "PM03"
    elif payment == "RestoPay Paylater":
        pmid = "PM04"
    else:
        pmid = "PM05"

    check_txi_post = query(f"""
        INSERT INTO transaction VALUES (
            '{email}', '{current_date}', '{street}', '{district}', '{city}', '{province}', 
            '{total_food}', '{diskon_value}', '{0}', '{0}', '{0}', '{pmid}', '{'PS01'}', '{'DF01'}', '{'vwixonb@sfgate.com'}');
        """)
    
    print(check_txi_post)

    for i in range(menu_count):

        menu_qty = int(request.POST['jumlah-' + str(i+1)])
        if menu_qty > 0:
            menu_name = menu_list[i][0] 
            menu_note = request.POST['catatan-' + str(i+1)]
            check_menu_post = query(f"""
                INSERT INTO transaction_food VALUES (
                    '{email}', '{current_date}', '{rname}', '{rbranch}', '{menu_name}', {menu_qty}, '{menu_note}'
                );
            """)
            print(check_menu_post)
        else:
            continue

    response = redirect('/trigger-4/list-pesanan/')
    response.set_cookie('current_date', current_date)
    response.set_cookie('vehicle', vehicle)
    response.set_cookie('payment', payment)

    return response

def list_pesanan(request):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()
    
    current_date = request.COOKIES.get('current_date')
    data['current_date'] = current_date

    data['transaction'] = query(f"""
        SELECT *
        FROM transaction t
        WHERE t.email = '{email}' AND t.datetime = '{current_date}';
    """)

    data['order'] = query(f"""
        SELECT tf.foodname, f.price, tf.amount, tf.amount*f.price AS subtotal
        FROM transaction_food tf
        INNER JOIN food f ON tf.foodname = f.foodname AND tf.rname = f.rname AND tf.rbranch = f.rbranch
        WHERE tf.email = '{email}' AND tf.datetime = '{current_date}';
    """)

    print(data['transaction'])
    print(data['order'])
    
    data['total_harga'] = data['transaction'][0][6]
    data['vehicle'] = request.COOKIES.get('vehicle')
    data['payment'] = request.COOKIES.get('payment')
    data['total_diskon'] = data['transaction'][0][7]
    data['biaya_pengantaran'] = data['transaction'][0][8]
    data['total_biaya'] = data['transaction'][0][9]

    if request.method != "POST":
        return render(request, 'tpel_pesanan_list.html', data)

    return redirect('/trigger-4/konfirmasi-pembayaran/')

def konfirmasi_pembayaran(request):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()
    status_date = str(date.now())[:23]
    
    current_date = request.COOKIES.get('current_date')
    data['waktu_pemesanan'] = current_date

    # NAMA PELANGGAN
    data['nama_pelanggan'] = query(f"""
        SELECT CONCAT(fname, ' ', lname)
        FROM user_acc
        WHERE email = '{email}';
    """)[0][0]

    print(data['nama_pelanggan'])

    transaction = query(f"""
        SELECT *
        FROM transaction t
        WHERE t.email = '{email}' AND t.datetime = '{current_date}';
    """)

    print(transaction)
    
    transaction_status = query(f"""
        INSERT INTO transaction_history VALUES (
            '{email}', '{current_date}', '{'TS01'}', '{status_date}'
        );
    """)

    data['pel_jalan'] = transaction[0][2]
    data['pel_kecamatan'] = transaction[0][3]
    data['pel_kota'] = transaction[0][4]
    data['pel_provinsi'] = transaction[0][5]


    data['order'] = query(f"""
        SELECT tf.foodname, f.price, tf.amount, tf.amount*f.price AS subtotal, tf.note, tf.rname, tf.rbranch
        FROM transaction_food tf
        INNER JOIN food f ON tf.foodname = f.foodname AND tf.rname = f.rname AND tf.rbranch = f.rbranch
        WHERE tf.email = '{email}' AND tf.datetime = '{current_date}';
    """)

    print(data['order'])

    rname = data['order'][0][5]
    rbranch = data['order'][0][6]

    restoran = query(f"""
        SELECT CONCAT(rname, ' ', rbranch) AS restoran, street, district, city, province 
        FROM restaurant
        WHERE rname = '{rname}' AND rbranch = '{rbranch}';
    """)

    print(restoran)

    data['restoran'] = restoran[0][0]
    data['rest_jalan'] = restoran[0][1]
    data['rest_kecamatan'] = restoran[0][2]
    data['rest_kota'] = restoran[0][3]
    data['rest_provinsi'] = restoran[0][4]
    
    data['total_harga_makanan'] = transaction[0][6]
    data['total_diskon'] = transaction[0][7]
    data['biaya_pengantaran'] = transaction[0][8]
    data['total_biaya'] = transaction[0][9]
    data['payment'] = request.COOKIES.get('payment')


    if request.method != "POST":
        return render(request, 'tpel_pesanan_pay.html', data)

    query(f"""
        UPDATE transaction
        SET psid = 'PS02'
        WHERE email = '{email}' AND datetime = '{current_date}';
        """)

    return redirect('/trigger-4/detail-pesanan/' + str(current_date) + '/')

def detail_pesanan(request, current_date):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()
    
    data['waktu_pemesanan'] = current_date

    # NAMA PELANGGAN
    data['nama_pelanggan'] = query(f"""
        SELECT CONCAT(fname, ' ', lname)
        FROM user_acc
        WHERE email = '{email}';
    """)[0][0]

    transaction = query(f"""
        SELECT *
        FROM transaction t
        WHERE t.email = '{email}' AND t.datetime = '{current_date}';
    """)

    data['pel_jalan'] = transaction[0][2]
    data['pel_kecamatan'] = transaction[0][3]
    data['pel_kota'] = transaction[0][4]
    data['pel_provinsi'] = transaction[0][5]


    data['order'] = query(f"""
        SELECT tf.foodname, f.price, tf.amount, tf.amount*f.price AS subtotal, tf.note, tf.rname, tf.rbranch
        FROM transaction_food tf
        INNER JOIN food f ON tf.foodname = f.foodname AND tf.rname = f.rname AND tf.rbranch = f.rbranch
        WHERE tf.email = '{email}' AND tf.datetime = '{current_date}';
    """)

    print(data['order'])

    rname = data['order'][0][5]
    rbranch = data['order'][0][6]

    restoran = query(f"""
        SELECT CONCAT(rname, ' ', rbranch) AS restoran, street, district, city, province 
        FROM restaurant
        WHERE rname = '{rname}' AND rbranch = '{rbranch}';
    """)

    print(restoran)

    data['restoran'] = restoran[0][0]
    data['rest_jalan'] = restoran[0][1]
    data['rest_kecamatan'] = restoran[0][2]
    data['rest_kota'] = restoran[0][3]
    data['rest_provinsi'] = restoran[0][4]
    
    data['total_harga_makanan'] = transaction[0][6]
    data['total_diskon'] = transaction[0][7]
    data['biaya_pengantaran'] = transaction[0][8]
    data['total_biaya'] = transaction[0][9]
    
    if transaction[0][11] == "PM01":
        data['payment'] = "RestoPay"
    elif transaction[0][11] == "PM02":
        data['payment'] = "Other e-Wallet"
    elif transaction[0][11] == "PM03":
        data['payment'] = "Bank Transfer"
    elif transaction[0][11] == "PM04":
        data['payment'] = "RestoPay Paylater"
    else:
        data['payment'] = "Cash on Delivery"

    if transaction[0][12] == "PS01":
        data['status_pembayaran'] = "Waiting for Payment"
    elif transaction[0][12] == "PS02":
        data['status_pembayaran'] = "Payment Successful"
    else:
        data['status_pembayaran'] = "Payment Unuccessful"

    transaction_history = query(f"""
        SELECT *
        FROM transaction_history th INNER JOIN transaction_status ts
        ON th.tsid = ts.id 
        WHERE email = '{email}' AND datetime = '{current_date}'
        ORDER BY tsid DESC;
    """)

    print(transaction_history)
    data['status_pesanan'] = transaction_history[0][5]

    email_kurir = transaction[0][14]

    if email_kurir != None:
        data_kurir = query(f"""
            SELECT CONCAT(ua.fname, ' ', ua.lname) AS name, c.platenum, c.vehicletype, c.vehiclebrand
            FROM user_acc ua INNER JOIN courier c ON ua.email = c.email
            WHERE ua.email = '{email_kurir}' AND c.email = '{email_kurir}';
        """)

        print(data_kurir)

        data['nama_kurir'] = data_kurir[0][0]
        data['plat_nomor'] = data_kurir[0][1]
        data['jenis_kendaraan'] = data_kurir[0][2]
        data['merk_kendaraan'] = data_kurir[0][3]
    else :
        data['nama_kurir'] = '-'
        data['plat_nomor'] = '-'
        data['jenis_kendaraan'] = '-'
        data['merk_kendaraan'] = '-'

    if request.method != "POST":
        return render(request, 'tpel_pesanan_pay.html', data)

    response = redirect('/trigger-4/daftar-pesanan/')
    
    response.delete_cookie('street')
    response.delete_cookie('district')
    response.delete_cookie('city')
    response.delete_cookie('province')

    response.delete_cookie('current_date')
    response.delete_cookie('payment')
    response.delete_cookie('vehicle')

    return response

def daftar_pesanan(request):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()
    
    data['transaction'] = query(f"""
        SELECT DISTINCT CONCAT(tf.rname, ' ', tf.rbranch) AS restoran, t.totalprice, cast(t.datetime AS TEXT), ts.name AS status
        FROM transaction_food tf
        INNER JOIN transaction t ON tf.email = t.email AND tf.datetime = t.datetime
        INNER JOIN transaction_history th ON t.email = th.email AND t.datetime = th.datetime
        INNER JOIN transaction_status ts ON th.tsid = ts.id
        WHERE tf.email = '{email}'
        ORDER BY datetime DESC;
    """)

    print(data['transaction'])

    if request.method != "POST":
        return render(request, 'tpel_user_pesanan_list.html', data)
    
    return redirect('/dashboard/detail/pelanggan/' + email + '/')


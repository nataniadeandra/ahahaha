from json import tool
from django.shortcuts import render, redirect
from sirest.utils import *
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
    max_id_get = get_query("SELECT MAX(id) FROM food_category;")
    max_id = max_id_get[0][0][-2:]
    id_kategori = "FC" + str(int(max_id) + 1).zfill(2);

    get_query(
        f"""
        INSERT INTO food_category VALUES ('{id_kategori}', '{nama_kategori}');
    """)

    return redirect('/trigger-4/list-kategori-makanan/')
    

def delete_kategori_makanan(request, id): 
    get_query(f"""
        DELETE FROM food_category 
        WHERE id = '{id}';
    """)

    return redirect('/trigger-4/list-kategori-makanan/')

def read_kategori_makanan(request):
    data = get_session_data(request)

    data['kategori_makanan'] = get_query("""
        SELECT * FROM food_category;
    """)

    return render(request, 'kategori_makanan_list.html', data)

# CR Transaksi Pelanggan Alamat
def create_alamat_pesanan(request):
    data = get_session_data(request)

    province_list = get_query("""
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

    restaurant_list = get_query(f"""
        SELECT rname, rbranch
        FROM restaurant
        WHERE province = '{province}';
    """)
    promo_list = get_query(f"""
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
    
    menu_list = get_query(f"""
        SELECT foodname, price
        FROM food
        WHERE rname = '{rname}' AND rbranch = '{rbranch}';
    """)
    payment_list = get_query(f"""
        SELECT name
        FROM payment_method;
    """)

    data['menu_list'] = menu_list
    data['payment_list'] = payment_list
    menu_count = len(menu_list)

    if request.method != "POST":
        return render(request, 'tpel_choose_restomenu_form.html', data)

    vehicle = request.POST['vehicle']
    payment = request.POST['payment']

    for i in range(menu_count):

        menu_qty = int(request.POST['jumlah-' + str(i+1)])
        if menu_qty > 0:
            menu_name = menu_list[i][0] 
            menu_note = request.POST['catatan-' + str(i+1)]
            get_query(
            f"""
            INSERT INTO transaction_food VALUES ('{email}', '{current_date}', '{rname}', '{rbranch}', '{menu_name}', {menu_qty}, '{menu_note}');
            """
            )
        else:
            continue

    response = redirect('/trigger-4/list-pesanan/')

    response.set_cookie('rname', rname)
    response.set_cookie('rbranch', rbranch)
    response.set_cookie('vehicle', vehicle)
    response.set_cookie('payment', payment)
    response.set_cookie('current_date', current_date)

    return response

def list_pesanan(request):
    data = get_session_data(request)
    email = str(request.session["email"]).strip()

    rname = request.COOKIES.get('rname')
    rbranch = request.COOKIES.get('rbranch')
    province = request.COOKIES.get('province')
    vehicle = request.COOKIES.get('vehicle')
    payment = request.COOKIES.get('payment')
    current_date = request.COOKIES.get('current_date')

    data['rname'] = rname
    data['rbranch'] = rbranch
    data['province'] = province
    data['vehicle'] = vehicle
    data['payment'] = payment
    data['current_date'] = current_date

    motor_fee = get_query(f"""
        SELECT motorfee FROM delivery_fee_per_km 
        WHERE province = '{province}';
    """)

    car_fee = get_query(f"""
        SELECT carfee FROM delivery_fee_per_km 
        WHERE province = '{province}';
    """)
    
    data['motor_fee'] = motor_fee
    data['car_fee'] = car_fee

    if vehicle == "Motor":
        vehicle_fee = motor_fee
    else:
        vehicle_fee = car_fee

    data['vehicle_fee'] = vehicle_fee

    data['order'] = get_query(f"""
        SELECT tf.foodname, f.price, tf.amount, tf.amount*f.price AS subtotal
        FROM transaction_food tf
        INNER JOIN food f ON tf.foodname = f.foodname AND tf.rname = f.rname AND tf.rbranch = f.rbranch;
    """)

    return render(request, 'tpel_pesanan_list.html', data)

def konfirmasi_pembayaran(request):
    return render(request, 'tpel_pesanan_pay.html')

def ringkasan_pesanan(request):
    return render(request, 'ringkasan_pesanan.html')
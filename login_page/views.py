from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import psycopg2
from sirest.utils import *
from util.query import query
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

def checkPassword(str):
 
    # initializing flag variable
    flag_l = False
    flag_n = False
 
    # checking for letter and numbers in
    # given string
    for i in str:
 
        # if string has letter
        if i.isalpha():
            flag_l = True
 
        # if string has number
        if i.isdigit():
            flag_n = True
 
    # returning and of flag
    # for checking required condition
    return flag_l and flag_n

# Login & Logout
def init(request):
    return render(request, 'init.html')

# def login(request):
#     return render(request, 'login.html')

def login(request):

    if request.method != "POST" and not is_authenticated(request):
        return render(request, 'login.html', {'title': "Login"})

    if is_authenticated(request):
        email = str(request.session["email"])
        password = str(request.session["password"])
    else:
        email = str(request.POST["email"])
        password = str(request.POST["password"])

    role = get_role(email, password)

    if role == "":
        if not is_authenticated(request):
            messages.error(request, 'Email atau password salah')
            return render(request, 'login.html', {'title': "Login"})
    else:
        request.session["email"] = email
        request.session["password"] = password
        request.session["role"] = role
        request.session.set_expiry(0)
        request.session.modified = True

    if role == "admin":
        return redirect("../../dashboard/admin/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")
    elif role == "courier":
        return redirect("../../dashboard/kurir/")

def logout(request):
    if not is_authenticated(request):
        return redirect("/login_page/login")

    request.session.flush()
    request.session.clear_expired()

    return redirect("/login_page/login")

# CRU Pengguna
# Choose Role Register
def register(request):
    return render(request, 'register.html')
# Create Admin
def register_admin(request):
    messages = {}
    messages['error'] = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        list_nama = nama.split()
        if (len(list_nama) == 1):
            fname = list_nama[0]
        else:
            fname = list_nama[0]
            lname = list_nama[1]
        no_hp = request.POST.get('no_hp')

        password_cek = checkPassword(password)
        if password_cek == False:
            print('halo')
            messages['error'] = True
            return render(request, 'register_admin.html', messages)

        email_cek = None
        email_cek = query(f"""
        SELECT * FROM USER_ACC
        WHERE email = '{email}'
        """)
        if email_cek != None:
            messages['error'] = True
            return render(request, 'register_admin.html', messages)

        query(f"""
        INSERT INTO sirest.USER_ACC
        VALUES ('{email}', '{password}', '{fname}', '{lname}', '{no_hp}')
        """)
        query(f"""
        INSERT INTO sirest.ADMIN
        VALUES ('{email}')
        """)

        role = get_role(email, password)
        if role == "":
            if not is_authenticated(request):
                messages.error(request, 'Email atau password salah')
                return render(request, 'login.html', {'title': "Login"})
            else:
                request.session["email"] = email
                request.session["password"] = password
                request.session["role"] = role
                request.session.set_expiry(0)
                request.session.modified = True
        return redirect("../../dashboard/admin/")
    
    return render(request, 'register_admin.html', messages)
# Create Cust
def register_cust(request):
    messages = {}
    messages['error'] = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        list_nama = nama.split()
        if (len(list_nama) == 1):
            fname = list_nama[0]
        else:
            fname = list_nama[0]
            lname = list_nama[1]
        no_hp = request.POST.get('no_hp')
        nik = request.POST.get('nik')
        nama_bank = request.POST.get('nama_bank')
        no_rek = request.POST.get('no_rek')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        jenis_kelamin = request.POST.get('jenis_kelamin')

        password_cek = checkPassword(password)
        if password_cek == False:
            print('halo')
            messages['error'] = True
            return render(request, 'register_cust.html', messages)

        email_cek = None
        email_cek = query(f"""
        SELECT * FROM USER_ACC
        WHERE email = '{email}'
        """)
        if email_cek != None:
            messages['error'] = True
            print('multiple')
            return render(request, 'register_cust.html', messages)
        
        query(f"""
        INSERT INTO sirest.USER_ACC
        VALUES ('{email}', '{password}', '{fname}', '{lname}', '{no_hp}')
        """)

        query(f"""
        INSERT INTO TRANSACTION_ACTOR
        VALUES ('{email}', '{nik}', '{nama_bank}', '{no_rek}', 0)
        """)

        query(f"""
        INSERT INTO CUSTOMER
        VALUES ('{email}', '{tanggal_lahir}', '{jenis_kelamin}')
        """)

        role = get_role(email, password)
        if role == "":
            if not is_authenticated(request):
                messages.error(request, 'Email atau password salah')
                return render(request, 'login.html', {'title': "Login"})
            else:
                request.session["email"] = email
                request.session["password"] = password
                request.session["role"] = role
                request.session.set_expiry(0)
                request.session.modified = True
        return redirect("../../dashboard/cust/")
    return render(request, 'register_cust.html', messages)
# Create Resto
def register_rest(request):
    messages = {}
    messages['error'] = False
    messages = {}
    messages['error'] = False
    province = query(f"""
    SELECT Province 
    FROM DELIVERY_FEE_PER_KM
    """)
    res_category = query("""
    SELECT Id, Name
    FROM RESTAURANT_CATEGORY
    """)
    messages['province'] = province
    messages['res_category'] = res_category
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        list_nama = nama.split()
        if (len(list_nama) == 1):
            fname = list_nama[0]
        else:
            fname = list_nama[0]
            lname = list_nama[1]
        no_hp = request.POST.get('no_hp')
        nik = request.POST.get('nik')
        nama_bank = request.POST.get('nama_bank')
        no_rek = request.POST.get('no_rek')
        nama_restoran = request.POST.get('nama_restoran')
        cabang = request.POST.get('cabang')
        no_telp = request.POST.get('no_telp')
        jalan = request.POST.get('jalan')
        kecamatan = request.POST.get('kecamatan')
        kota = request.POST.get('kota')
        provinsi = request.POST.get('provinsi')
        kategori_restoran = request.POST.get('kategori_restoran')

        password_cek = checkPassword(password)
        if password_cek == False:
            print('halo')
            messages['error'] = True
            return render(request, 'register_rest.html', messages)

        email_cek = None
        email_cek = query(f"""
        SELECT * FROM USER_ACC
        WHERE email = '{email}'
        """)
        if email_cek != None:
            messages['error'] = True
            return render(request, 'register_rest.html', messages)

        query(f"""
        INSERT INTO sirest.USER_ACC
        VALUES ('{email}', '{password}', '{fname}', '{lname}', '{no_hp}')
        """)

        query(f"""
        INSERT INTO TRANSACTION_ACTOR
        VALUES ('{email}', '{nik}', '{nama_bank}', '{no_rek}', 0)
        """)

        query(f"""
        INSERT INTO RESTAURANT
        VALUES ('{email}', '{nama_restoran}', '{cabang}', '{no_telp}', '{jalan}', '{kecamatan}', '{kota}', '{provinsi}', '{kategori_restoran}')
        """)

        role = get_role(email, password)
        if role == "":
            if not is_authenticated(request):
                messages.error(request, 'Email atau password salah')
                return render(request, 'login.html', {'title': "Login"})
            else:
                request.session["email"] = email
                request.session["password"] = password
                request.session["role"] = role
                request.session.set_expiry(0)
                request.session.modified = True
        return redirect("../../dashboard/rest/")
    return render(request, 'register_rest.html', messages)
# Create Cour
def register_cour(request):
    messages = {}
    messages['error'] = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        list_nama = nama.split()
        if (len(list_nama) == 1):
            fname = list_nama[0]
        else:
            fname = list_nama[0]
            lname = list_nama[1]
        no_hp = request.POST.get('no_hp')
        nik = request.POST.get('nik')
        nama_bank = request.POST.get('nama_bank')
        no_rek = request.POST.get('no_rek')
        plat_no = request.POST.get('plat_no')
        no_sim = request.POST.get('no_sim')
        jenis_kendaraan = request.POST.get('jenis_kendaraan')
        merk_kendaraan = request.POST.get('merk_kendaraan')

        password_cek = checkPassword(password)
        if password_cek == False:
            print('halo')
            messages['error'] = True
            return render(request, 'register_cour.html', messages)

        email_cek = None
        email_cek = query(f"""
        SELECT * FROM USER_ACC
        WHERE email = '{email}'
        """)
        if email_cek != None:
            messages['error'] = True
            return render(request, 'register_cour.html', messages)

        query(f"""
        INSERT INTO sirest.USER_ACC
        VALUES ('{email}', '{password}', '{fname}', '{lname}', '{no_hp}')
        """)

        query(f"""
        INSERT INTO TRANSACTION_ACTOR
        VALUES ('{email}', '{nik}', '{nama_bank}', '{no_rek}', 0)
        """)

        query(f"""
        INSERT INTO COURIER
        VALUES ('{email}', '{plat_no}', '{no_sim}', '{jenis_kendaraan}', '{merk_kendaraan}')
        """)

        role = get_role(email, password)
        if role == "":
            if not is_authenticated(request):
                messages.error(request, 'Email atau password salah')
                return render(request, 'login.html', {'title': "Login"})
            else:
                request.session["email"] = email
                request.session["password"] = password
                request.session["role"] = role
                request.session.set_expiry(0)
                request.session.modified = True
        return redirect("../../dashboard/cour/")
        

    return render(request, 'register_cour.html', messages)

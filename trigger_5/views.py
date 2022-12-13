from django.shortcuts import render, redirect
from .forms import bahanMakananForm, kategoriRestoranForm
from util.query import query
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from sirest.utils import get_role, is_authenticated
from datetime import datetime, timedelta
# Create your views here.
def show_bahan_makanan(request):
    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
        return response

    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
        return response

    role = get_role(request.session['email'], request.session['password'])
    if role == "courier":
        return redirect("../../dashboard/kurir/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")

    data = {}
    bahan_makanan = query(f"""
    SELECT Id, Name
    FROM INGREDIENT 
    """)
    # cek referensi
    bahan_makanan_check = query("""
    SELECT Id
    FROM INGREDIENT I, FOOD_INGREDIENT FI
    WHERE Id = Ingredient
    """)
    # print(bahan_makanan_check)
    # print(bahan_makanan)
    list_bahan_makanan = []
    list_bahan_dependecies = [False]*len(bahan_makanan)
    for i in range(len(bahan_makanan_check)):
        idx = int(bahan_makanan_check[i][0][3:])-1
        if list_bahan_dependecies[idx] == False:
            list_bahan_dependecies[idx] = True
    for i in range(len(bahan_makanan)):
        list_bahan_makanan.append({
            'id' : bahan_makanan[i][0],
            'name' : bahan_makanan[i][1],
            'index' : i+1,
            'is_referenced' : list_bahan_dependecies[i] 
        })
    data['item_list'] = list_bahan_makanan
    print(data['item_list'])
    return render(request, 'bahan_makanan.html', data)

def create_bahan_makanan(request):
    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
        return response

    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
        return response

    role = get_role(request.session['email'], request.session['password'])
    if role == "courier":
        return redirect("../../dashboard/kurir/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")

    role = get_role(request.session['email'], request.session['password'])
    if role == "courier":
        return redirect("../../dashboard/kurir/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")
    
    form_gen = bahanMakananForm()
    if request.method == 'POST':
        form = bahanMakananForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            rc_count = query(f"""
            SELECT COUNT(Id)
            FROM INGREDIENT
            """)
            id = 'ING' + str(rc_count)
            query(f"""
            INSERT INTO INGREDIENT
            VALUES ('{id}', '{name}')
            """)
            response = HttpResponseRedirect(reverse("trigger_5:show_bahan_makanan"))
            return response
    context = {
        'form' : form_gen
    }
    return render(request, 'bahan_makanan_create.html', context)

def show_kategori_restoran(request):
    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
        return response

    role = get_role(request.session['email'], request.session['password'])
    if role == "courier":
        return redirect("../../dashboard/kurir/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")
    
    data = {}
    print(request.session['email'])
    kategori_restoran = query(f"""
    SELECT Id, Name
    FROM RESTAURANT_CATEGORY
    """)

    kategori_restoran_check = query("""
    SELECT Id
    FROM RESTAURANT_CATEGORY, RESTAURANT
    WHERE Id = RCategory
    """)

    list_restoran_dependecies = [False]*len(kategori_restoran)
    for i in range(len(kategori_restoran_check)):
        idx = int(kategori_restoran_check[i][0][2:])-1
        if list_restoran_dependecies[idx] == False:
            list_restoran_dependecies[idx] = True
    
    list_kategori_restoran = []
    for i in range(len(kategori_restoran)):
        list_kategori_restoran.append({
            'id' : kategori_restoran[i][0],
            'name' : kategori_restoran[i][1],
            'index' : i+1,
            'is_referenced' : list_restoran_dependecies[i]
        })

    

    data['item_list'] = list_kategori_restoran
    print(data['item_list'])
    return render(request, 'kategori_restoran.html', data)

def delete_bahan_makanan(request, id):
    print(id)
    query(f"""
    DELETE FROM INGREDIENT
    WHERE Id = '{id}'
    """)
    response = HttpResponseRedirect(reverse("trigger_5:show_bahan_makanan"))
    return response

def create_kategori_restoran(request):
    role = get_role(request.session['email'], request.session['password'])
    if role == "courier":
        return redirect("../../dashboard/kurir/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")

    if request.method == 'POST':
        form = kategoriRestoranForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            rc_count = query(f"""
            SELECT COUNT(Id)
            FROM RESTAURANT_CATEGORY
            """)
            id = 'RC' + str(rc_count)
            query(f"""
            INSERT INTO RESTAURANT_CATEGORY
            VALUES ('{id}', '{name}')
            """)
            response = HttpResponseRedirect(reverse("trigger_5:show_kategori_restoran"))
            return response
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
    if is_authenticated(request) == False:
        response = HttpResponseRedirect(reverse("login_page:login"))
    role = get_role(request.session['email'], request.session['password'])
    if role == "admin":
        return redirect("../../dashboard/admin/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")
    
    quert_res = query(f"""
    SELECT Rname, Rbranch, Fname, Lname, T.Datetime, Name
    FROM TRANSACTION T, TRANSACTION_FOOD TF, USER_ACC U, TRANSACTION_HISTORY TH, TRANSACTION_STATUS TS
    WHERE CourierId = '{request.session['email']}' AND T.Email = TF.Email AND T.Datetime = TF.Datetime
    AND T.Email = U.Email AND T.Email = TH.Email AND T.Datetime = TH.Datetime AND TH.TSId = TS.Id
    """)
    # print (quert_res)
    # restoran_cabang = query(f"""
    # SELECT Rname, Rbranch
    # FROM TRANSACTION T, TRANSACTION_FOOD TF
    # WHERE CourierId = '{request.session['email']}' AND T.Email = TF.Email AND T.Datetime = TF.Datetime
    # """)

    # nama_pelanggan = query(f"""
    # SELECT Fname, Lname
    # FROM TRANSACTION T, USER_ACC U
    # WHERE T.Email = U.Email AND CourierId = '{request.session['email']}'
    # """)

    # waktu_pesanan = query(f"""
    # SELECT Datetime 
    # FROM TRANSACTION
    # WHERE CourierId = '{request.session['email']}'
    # """)

    # status_pesanan = query(f"""
    # SELECT Name
    # FROM TRANSACTION T, TRANSACTION_HISTORY TH, TRANSACTION_STATUS TS
    # WHERE T.Email = TH.Email AND T.Datetime = TH.Datetime AND TH.TSId = TS.Id AND CourierId = '{request.session['email']}'
    # """)
    # print(get_role(request.session['email'], '84jlaFTSs9'))
    # print(request.session['email'])
    # print(restoran_cabang)
    # print(nama_pelanggan)
    # print(waktu_pesanan)
    # print(status_pesanan)
    # print(len(quert_res))
    # print()
    # print(quert_res[0][0])
    item_list = []
    # print(type(waktu_pesanan[0][0]))
    # print(waktu_pesanan[0][0])
    for i in range(len(quert_res)):
        if(quert_res[i][5] == 'Delivering Order'):
            item_list.append({'restoran': quert_res[i][0],
                            'cabang' : quert_res[i][1],
                            'nama_pelanggan' : quert_res[i][2] + " " + quert_res[i][3],
                            'waktu_pesanan' : quert_res[i][4].strftime("%m-%d-%Y %H:%M:%S"),
                            'status_pesanan' : quert_res[i][5]}
                            )
    for i in range(len(item_list)):
        item_list[i]['index'] = i+1
    # data['restoran_cabang'] = restoran_cabang
    # data['nama_pelanggan'] = nama_pelanggan
    # data['waktu_pesanan'] = waktu_pesanan
    # data['status_pesanan'] = status_pesanan
    print(item_list)
    data = {}
    data = {'item_list' : item_list}
    print(data)

    return render(request, 'transaksi_pesanan_kurir.html', data)

def show_transaksi_pesanan_kurir_detail(request, restoran, cabang, nama_pelanggan, waktu_pesanan, status_pesanan):
    # print(restoran, cabang, nama_pelanggan, waktu_pesanan, status_pesanan)
    waktu_pesanan_min = datetime.strptime(waktu_pesanan, '%m-%d-%Y %H:%M:%S')
    print(waktu_pesanan_min)
    waktu_pesanan_max = waktu_pesanan_min + timedelta(seconds=1)
    fname, lname = nama_pelanggan.split()
    email = query(f"""
    SELECT email
    FROM USER_ACC
    WHERE Fname = '{fname}' AND Lname = '{lname}'
    """)[0][0]

    transaksi = query(f"""
    SELECT Street, District, City, Province, TotalFood, TotalDiscount, DeliveryFee, TotalPrice 
    FROM TRANSACTION
    WHERE Email = '{email}' AND  (Datetime <= '{waktu_pesanan_max}' and Datetime >= '{waktu_pesanan_min}')
    """)

    restoran_detail = query(f"""
    SELECT Rname, Rbranch, Street, District, City, Province
    FROM RESTAURANT
    WHERE Rname = '{restoran}' AND Rbranch = '{cabang}'
    """)

    makanan = query(f"""
    SELECT FoodName, Note 
    FROM TRANSACTION_FOOD 
    WHERE Rname = '{restoran}' AND Rbranch = '{cabang}' AND Email = '{email}' AND  (Datetime <= '{waktu_pesanan_max}' and Datetime >= '{waktu_pesanan_min}')
    """)

    status_pembayaran = query(f"""
    SELECT Name
    FROM TRANSACTION T, PAYMENT_STATUS PS
    WHERE T.Email = '{email}' AND  (Datetime <= '{waktu_pesanan_max}' and Datetime >= '{waktu_pesanan_min}') AND T.PSId = PS.Id
    """)

    jenis_pembayaran = query(f"""
    SELECT Name
    FROM TRANSACTION T, PAYMENT_METHOD PM
    WHERE T.Email = '{email}' AND  (Datetime <= '{waktu_pesanan_max}' and Datetime >= '{waktu_pesanan_min}') AND T.PMId = PM.Id
    """)

    kurir = query(f"""
    SELECT Fname, Lname, PlateNum, VehicleType, VehicleBrand
    FROM COURIER, USER_ACC
    WHERE COURIER.Email = '{request.session['email']}' AND COURIER.email = USER_ACC.email
    """
    )
    data = {}
    data['transaksi'] = transaksi[0]
    data['restoran_detail'] = restoran_detail[0]
    
    makanan_list = []
    for i in range(len(makanan)):
        makanan_list.append({
            'foodname' : makanan[i][0],
            'Note' : makanan[i][1],
            'index' : i+1
        })
    data['makanan'] = makanan_list
    data['status_pembayaran'] = status_pembayaran[0]
    data['jenis_pembayaran'] = jenis_pembayaran[0]
    data['status_pesanan'] = status_pesanan
    data['nama_pelanggan'] = nama_pelanggan
    data['kurir'] = kurir[0]

    return render(request, 'transaksi_pesanan_kurir_detail.html', data)

def update_transaksi_pesanan_kurir(request, nama_pelanggan, waktu_pesanan):
    
    fname, lname = nama_pelanggan.split()
    waktu_pesanan_min = datetime.strptime(waktu_pesanan, '%m-%d-%Y %H:%M:%S')
    waktu_pesanan_max = waktu_pesanan_min + timedelta(seconds=1)
    print(fname, lname, waktu_pesanan_min, waktu_pesanan_max)
    email = query(f"""
    SELECT email
    FROM USER_ACC
    WHERE Fname = '{fname}' AND Lname = '{lname}'
    """)[0][0]

    query(f"""
    UPDATE TRANSACTION_HISTORY
    SET TSId = 'TS04'
    WHERE Email = '{email}' AND  (Datetime <= '{waktu_pesanan_max}' and Datetime >= '{waktu_pesanan_min}') AND TSId = 'TS03'
    """)
    
    response = HttpResponseRedirect(reverse("trigger_5:show_transaksi_pesanan_kurir"))
    return response
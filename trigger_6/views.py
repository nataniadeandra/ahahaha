from django.shortcuts import render


# Create your views here.

# RU Riwayat Transaksi Pemesanan
# Read Pelanggan
def show_riwayat_txi_cust(request):
    return render(request, 'riwayat_txi_cust.html')
# Read Resto
def show_riwayat_txi_rest(request):
    return render(request, 'riwayat_txi_rest.html')
# Read Kurir
def show_riwayat_txi_cour(request):
    return render(request, 'riwayat_txi_cour.html')
# Read Pelanggan, Resto, Kurir
def show_detail_riwayat_txi(request, pk):
    return render(request, 'detail_riwayat_txi.html')
# Update Pelanggan
def form_penilaian(request, pk):
    return render(request, 'form_penilaian.html')

# CRUD Promo Admin
# Create Admin
def form_promo_home(request):
    return render(request, 'form_promo_home.html')
# Create Admin
def form_promo_minimumtxi(request):
    return render(request, 'form_promo_minimumtxi.html')
# Create Admin
def form_promo_specialday(request):
    return render(request, 'form_promo_specialday.html')
# Update Admin
def form_ubah_promo_minimumtxi(request, pk):
    return render(request, 'form_ubah_promo_minimumtxi.html')
# Update Admin
def form_ubah_promo_specialday(request, pk):
    return render(request, 'form_ubah_promo_specialday.html')
# Read Admin
def show_promo_admin(request):
    return render(request, 'daftar_promo_admin.html')
# Read Admin
def show_detail_promo_admin(request, pk):
    return render(request, 'detail_promo_admin.html')

# CRUD Promo Resto
# Read Resto
def show_promo_rest(request):
    return render(request, 'daftar_promo_rest.html')
# Read Resto
def show_detail_promo_rest(request, pk):
    return render(request, 'detail_promo_rest.html')
# Create Resto
def add_promo_rest(request):
    return render(request, 'add_promo_rest.html')
# Update Resto
def ubah_promo_rest(request):
    return render(request, 'ubah_promo_rest.html')
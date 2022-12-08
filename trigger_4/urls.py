from django.urls import path
from . import views

app_name = 'trigger_4'

urlpatterns = [
    # Kategori Makanan
    path('form-kategori-makanan/', views.create_kategori_makanan, name='form-kategori-makanan'),
    path('kategori-makanan-list/', views.read_kategori_makanan, name='kategori-makanan-list'),
    path('kategori-makanan-list/hapus/<id>', views.read_kategori_makanan, name='kategori-makanan-list'),

    path('form-alamat-pesanan/', views.create_alamat_pesanan, name='form-alamat-pesanan'),
    path('daftar-pesanan/', views.daftar_pesanan, name='daftar-pesanan'),
    path('form-alamat-pesanan/', views.create_alamat_pesanan, name='form-alamat-pesanan'),
    path('konfirmasi-pembayaran/', views.konfirmasi_pembayaran, name='konfirmasi-pembayaran'),
    path('pemilihan-detail-pesanan/', views.pemilihan_detail_pesanan, name='pemilihan-detail-pesanan'),
    path('pemilihan-restoran/', views.pemilihan_restoran, name='pemilihan-restoran'),
    path('pesanan-berlangsung/', views.pesanan_berlangsung, name='pesanan-berlangsung'),
    path('ringkasan-pesanan/', views.ringkasan_pesanan, name='ringkasan-pesanan'), 
]
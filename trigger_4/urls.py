from django.urls import path
from . import views

app_name = 'trigger_4'

urlpatterns = [
    # Kategori Makanan
    path('form-kategori-makanan/', views.create_kategori_makanan, name='form-kategori-makanan'),
    path('list-kategori-makanan/', views.read_kategori_makanan, name='list-kategori-makanan'),
    path('hapus-kategori-makanan/<str:id>/', views.delete_kategori_makanan, name='hapus-kategori-makanan'),
    
    # Pesan Makanan (POV Pelanggan)
    path('form-alamat-pesanan/', views.create_alamat_pesanan, name='form-alamat-pesanan'),
    path('list-resto/<str:province>/', views.pilih_restolist_pesanan, name='list-resto'),
    path('list-menu/<str:rname>/<str:rbranch>/', views.pilih_restomenu_pesanan, name='list-menu'),
    path('list-pesanan/', views.list_pesanan, name='list-pesanan'),
    path('konfirmasi-pembayaran/', views.konfirmasi_pembayaran, name='konfirmasi-pembayaran'),
]
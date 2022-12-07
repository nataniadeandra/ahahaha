from django.urls import path
from . import views

app_name = 'trigger_5'

urlpatterns = [
    path('bahan-makanan/', views.show_bahan_makanan, name='show_bahan_makanan'),
    path('kategori-restoran/', views.show_kategori_restoran, name='show_kategori_restoran'),
    path('bahan-makanan-create/', views.create_bahan_makanan, name='create_bahan_makanan'),
    path('kategori-restoran-create/', views.create_kategori_restoran, name='create_kategori_restoran'),
    path('transaksi-pesanan-kurir/', views.show_transaksi_pesanan_kurir, name='show_transaksi_pesanan_kurir'),
    path('transaksi-pesanan-kurir-detail/', views.show_transaksi_pesanan_kurir_detail, name='show_transaksi_pesanan_kurir_detail'),
    path('kategori-restoran-delete/<str:id>', views.delete_kategori_restoran, name='delete_kategori_restoran')
]
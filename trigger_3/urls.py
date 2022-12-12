from django.urls import path
from . import views

app_name = 'trigger_3'

urlpatterns = [
    path('makanan_add/', views.tambah_makanan, name='halaman_tambah_makanan'),
    path('makanan_update/', views.update_makanan, name='halaman_update_makanan'),
    path('makanan/', views.makanan_page, name='halaman_makanan'),
    path('restoran_makanan_detail/', views.restoran_detail_makanan, name='halaman_detail_makanan_restoran'),
    path('restoran_makanan_menu/', views.restoran_menu_makanan, name='halaman_menu_makanan_restoran'),
    path('restoran_makanan/', views.restoran_makanan_page, name='halaman_makanan_restoran'),
    path('tarif_pengiriman_add/', views.tambah_tarif_pengiriman, name='halaman_tambah_tarif_pengiriman'),
    path('tarif_pengiriman_update/', views.update_tarif_pengiriman, name='halaman_update_tarif_pengiriman'),
    path('tarif_pengiriman/', views.tarif_pengiriman_page, name='halaman_tarif_pengiriman'),
]
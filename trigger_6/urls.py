from django.urls import path
from . import views

app_name = 'trigger_6'

urlpatterns = [
    path('riwayat_transaksi_cust/', views.show_riwayat_txi_cust, name='riwayat_transaksi_cust'),
    path('riwayat_transaksi_rest/', views.show_riwayat_txi_rest, name='riwayat_transaksi_rest'),
    path('riwayat_transaksi_cour/', views.show_riwayat_txi_cour, name='riwayat_transaksi_cour'),
    path('detail_riwayat_transaksi/<int:pk>/', views.show_detail_riwayat_txi, name='detail_riwayat_transaksi'),
    path('form_penilaian/<int:pk>/', views.form_penilaian, name='form_penilaian'),
    path('form_promo/', views.form_promo_home, name='form_promo_home'),
    path('form_promo/minimumtxi/', views.form_promo_minimumtxi, name='form_promo_minimumtxi'),
    path('form_promo/specialday/', views.form_promo_specialday, name='form_promo_specialday'),
    path('daftar_promo/', views.show_promo_admin, name='daftar_promo'),
    path('daftar_promo/detail/<int:pk>/', views.show_detail_promo_admin, name='daftar_promo_detail'),
    path('form_promo/ubah/specialday/<int:pk>/', views.form_ubah_promo_specialday, name='form_ubah_promo_specialday'),
    path('form_promo/ubah/minimumtxi/<int:pk>/', views.form_ubah_promo_minimumtxi, name='form_ubah_promo_minimumtxi'),
    path('daftar_promo_rest/', views.show_promo_rest, name='daftar_promo_rest'),
    path('daftar_promo_rest/detail/<int:pk>/', views.show_detail_promo_rest, name='daftar_promo_rest_detail'),
    path('add_promo_rest/', views.add_promo_rest, name='add_promo_rest'),
    path('ubah_promo_rest/', views.ubah_promo_rest, name='ubah_promo_rest'),
]
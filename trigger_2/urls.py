from django.urls import path
from .views import create_jam_operasional, delete_jam_operasional, detail_transaksi_pesanan_restoran, read_jam_operasional, read_resto_pay, isi_resto_pay, read_transaksi_pesanan_restoran, tarik_resto_pay, update_jam_operasional, update_transaksi_pesanan_restoran

app_name = "trigger_2"

urlpatterns = [
    path("restopay/read/", read_resto_pay, name = "read_resto_pay"),
    path("restopay/isi/", isi_resto_pay, name = "isi_resto_pay"),
    path("restopay/tarik/", tarik_resto_pay, name = "tarik_resto_pay"),
    
    path("transaksipesanan/restoran/read/", read_transaksi_pesanan_restoran, name = "read_transaksi_pesanan_restoran"),
    path("transaksipesanan/restoran/update/<str:email>/<str:datetime>/", update_transaksi_pesanan_restoran, name = "update_transaksi_pesanan_restoran"),
    path("transaksipesanan/restoran/detail/<str:email>/<str:datetime>/", detail_transaksi_pesanan_restoran, name = "detail_transaksi_pesanan_restoran"),

    path("jamoperasional/create/", create_jam_operasional, name = "create_jam_operasional"),
    path("jamoperasional/read/", read_jam_operasional, name = "read_jam_operasional"),
    path("jamoperasional/update/<str:day>/", update_jam_operasional, name = "update_jam_operasional"),
    path("jamoperasional/delete/<str:day>/", delete_jam_operasional, name = "delete_jam_operasional"),
]
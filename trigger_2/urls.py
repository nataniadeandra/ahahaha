from django.urls import path
from .views import create_jam_operasional, delete_jam_operasional, read_jam_operasional, read_resto_pay, isi_resto_pay, tarik_resto_pay, update_jam_operasional

app_name = "trigger_2"

urlpatterns = [
    path("restopay/read/", read_resto_pay, name = "read_resto_pay"),
    path("restopay/isi/<int:pk>/", isi_resto_pay, name = "isi_resto_pay"),
    path("restopay/tarik/<int:pk>/", tarik_resto_pay, name = "tarik_resto_pay"),
    path("jamoperasional/create/", create_jam_operasional, name = "create_jam_operasional"),
    path("jamoperasional/read/", read_jam_operasional, name = "read_jam_operasional"),
    path("jamoperasional/update/<int:pk>/", update_jam_operasional, name = "update_jam_operasional"),
    path("jamoperasional/delete/<int:pk>/", delete_jam_operasional, name = "delete_jam_operasional"),
]
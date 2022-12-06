from django.urls import path
from dashboard.views import dashboard_kurir, dashboard_pelanggan, dashboard_restoran, detail_kurir, detail_pelanggan, detail_restoran

app_name = "dashboard"

urlpatterns = [
    path("pelanggan/", dashboard_pelanggan, name = "dashboard_pelanggan"),
    path("restoran/", dashboard_restoran, name = "dashboard_resto"),
    path("kurir/", dashboard_kurir, name = "dashboard_kurir"),
    path("detail/pelanggan/", detail_pelanggan, name = "detail_pelanggan"),
    path("detail/restoran/", detail_restoran, name = "detail_resto"),
    path("detail/kurir/", detail_kurir, name = "detail_kurir"),
]
from django.urls import path
from dashboard.views import dashboard_kurir, dashboard_pelanggan, dashboard_restoran

app_name = "dashboard"

urlpatterns = [
    path("pelanggan/", dashboard_pelanggan, name = "dashboard_pelanggan"),
    path("restoran/", dashboard_restoran, name = "dashboard_resto"),
    path("kurir/", dashboard_kurir, name = "dashboard_kurir"),
]
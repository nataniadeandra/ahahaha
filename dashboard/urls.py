from django.urls import path
from dashboard.views import dashboard_kurir, dashboard_pelanggan, dashboard_restoran, dashboard_admin, detail_kurir, detail_pelanggan, detail_restoran

app_name = "dashboard"

urlpatterns = [
    path("admin/", dashboard_admin, name = "dashboard_admin"),
    path("pelanggan/", dashboard_pelanggan, name = "dashboard_pelanggan"),
    path("restoran/", dashboard_restoran, name = "dashboard_resto"),
    path("kurir/", dashboard_kurir, name = "dashboard_kurir"),
    path("detail/pelanggan/<str:email>/", detail_pelanggan, name = "detail_pelanggan"),
    path("detail/restoran/<str:email>/", detail_restoran, name = "detail_resto"),
    path("detail/kurir/<str:email>/", detail_kurir, name = "detail_kurir"),
]
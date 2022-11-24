from django.urls import path
from dashboard.views import dashboard_kurir, dashboard_pelanggan, dashboard_restoran, detail_kurir, detail_pelanggan, detail_restoran

app_name = "dashboard"

urlpatterns = [
    path("pelanggan/<int:pk>/", dashboard_pelanggan, name = "dashboard_pelanggan"),
    path("restoran/<int:pk>/", dashboard_restoran, name = "dashboard_resto"),
    path("kurir/<int:pk>/", dashboard_kurir, name = "dashboard_kurir"),
    path("detail/pelanggan/<int:pk>/", detail_pelanggan, name = "detail_pelanggan"),
    path("detail/restoran/<int:pk>/", detail_restoran, name = "detail_resto"),
    path("detail/kurir/<int:pk>/", detail_kurir, name = "detail_kurir"),
]
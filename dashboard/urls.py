from django.urls import path
from dashboard.views import dashboard_kurir, dashboard_pelanggan, dashboard_restoran

app_name = "dashboard"

urlpatterns = [
    path("pelanggan/<int:pk>/", dashboard_pelanggan, name = "dashboard_pelanggan"),
    path("restoran/<int:pk>/", dashboard_restoran, name = "dashboard_resto"),
    path("kurir/<int:pk>/", dashboard_kurir, name = "dashboard_kurir"),
]
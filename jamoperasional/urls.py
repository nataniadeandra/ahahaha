from django.urls import path
from .views import create_jam_operasional, read_jam_operasional, update_jam_operasional, delete_jam_operasional

app_name = "jamoperasional"

urlpatterns = [
    path("create/", create_jam_operasional, name = "create_jam_operasional"),
    path("read/", read_jam_operasional, name = "read_jam_operasional"),
    path("update/<int:pk>/", update_jam_operasional, name = "update_jam_operasional"),
    path("delete/<int:pk>/", delete_jam_operasional, name = "delete_jam_operasional"),
]
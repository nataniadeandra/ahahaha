from django.shortcuts import render

# Create your views here.

# Login & Logout
def init(request):
    return render(request, 'init.html')
def login(request):
    return render(request, 'login.html')

# CRU Pengguna
# Choose Role Register
def register(request):
    return render(request, 'register.html')
# Create Admin
def register_admin(request):
    return render(request, 'register_admin.html')
# Create Cust
def register_cust(request):
    return render(request, 'register_cust.html')
# Create Resto
def register_rest(request):
    return render(request, 'register_rest.html')
# Create Cour
def register_cour(request):
    return render(request, 'register_cour.html')

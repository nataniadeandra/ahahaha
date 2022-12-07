from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sirest.utils import *

# Login & Logout
def init(request):
    return render(request, 'init.html')

# def login(request):
#     return render(request, 'login.html')

def login(request):

    if request.method != "POST" and not is_authenticated(request):
        return render(request, 'login.html', {'title': "Login"})

    if is_authenticated(request):
        email = str(request.session["email"])
        password = str(request.session["password"])
    else:
        email = str(request.POST["email"])
        password = str(request.POST["password"])

    role = get_role(email, password)

    if role == "":
        if not is_authenticated(request):
            messages.error(request, 'Email atau password salah')
            return render(request, 'login.html', {'title': "Login"})
    else:
        request.session["email"] = email
        request.session["password"] = password
        request.session["role"] = role
        request.session.set_expiry(0)
        request.session.modified = True

    if role == "admin":
        return redirect("../../dashboard/admin/")
    elif role == "customer":
        return redirect("../../dashboard/pelanggan/")
    elif role == "restaurant":
        return redirect("../../dashboard/restoran/")
    elif role == "courier":
        return redirect("../../dashboard/kurir/")

def logout(request):

    if not is_authenticated(request):
        return redirect("/login_page/login")

    request.session.flush()
    request.session.clear_expired()

    return redirect("/login_page/login")

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

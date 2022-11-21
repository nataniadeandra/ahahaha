from django.shortcuts import redirect, render

# Create your views here.
def read_resto_pay(request):
    return render(request, 'read_resto_pay.html')

def isi_resto_pay(request, pk):
    return render(request, 'isi_resto_pay.html')

def tarik_resto_pay(request, pk):
    return render(request, 'tarik_resto_pay.html')

def create_jam_operasional(request):
    return render(request, 'create_jam_operasional.html')

def read_jam_operasional(request):
    return render(request, 'read_jam_operasional.html')

def update_jam_operasional(request, pk):
    return render(request, 'update_jam_operasional.html')

def delete_jam_operasional(request, pk):
    return redirect('../../read/')
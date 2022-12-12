from django.shortcuts import render

# Create your views here.

def tambah_makanan(request):
    return render(request, 'makanan_add.html')

def update_makanan(request):
    return render(request, 'makanan_update.html')

def makanan_page(request, pk):
    return render(request, 'makanan.html')

def restoran_detail_makanan(request, pk):
    return render(request, 'restoran_makanan_detail.html')

def restoran_menu_makanan(request):
    return render(request, 'restoran_makanan_menu.html')

def restoran_makanan_page(request):
    return render(request, 'restoran_makanan.html')

def tarif_pengiriman_page(request):
    return render(request, 'tarif_pengiriman.html')

def tambah_tarif_pengiriman(request, pk):
    return render(request, 'tarif_pengiriman_add.html')

def update_tarif_pengiriman(request, pk):
    return render(request, 'tarif_pengiriman_update.html')
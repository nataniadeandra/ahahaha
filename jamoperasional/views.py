from django.shortcuts import redirect, render

# Create your views here.
def create_jam_operasional(request):
    return render(request, 'create_jam_operasional.html')

def read_jam_operasional(request):
    return render(request, 'read_jam_operasional.html')

def update_jam_operasional(request, pk):
    return render(request, 'update_jam_operasional.html')

def delete_jam_operasional(request, pk):
    return redirect('jamoperasional/read_jam_operasional/')
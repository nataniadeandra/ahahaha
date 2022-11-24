from django import forms

class kategoriMakananForm(forms.Form):

    name = forms.CharField(
        label = "Nama Kategori Makanan",
        max_length= 50,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )

PROVINCE = ['DKI Jakarta', 'Banten', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur',
            'Bali', 'DI Yogyakarta', 'Kalimantan Utara', 'Kalimantan Barat', 'Riau']

class pengisianAlamatPesananMakananForm(forms.Form):
        jalan = forms.CharField(
        label = "Jalan",
        max_length= 50,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )
        kecamatan = forms.CharField(
        label = "Kecamatan",
        max_length= 50,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )
        kota = forms.CharField(
        label = "Kota",
        max_length= 50,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )
        provinsi = forms.CharField(
            label = "Provinsi",
            widget = forms.Select(choices=PROVINCE)
    )
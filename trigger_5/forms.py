from django import forms

class kategoriRestoranForm(forms.Form):

    name = forms.CharField(
        label = "Nama Kategori Restoran",
        max_length= 50,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )

class bahanMakananForm(forms.Form):

    name = forms.CharField(
        label = "Nama Bahan Makanan",
        max_length= 25,
        required= True,
        widget = forms.TextInput(attrs = {'class' : 'input', 'placeholder' : 'Name','class' : 'form-control'})
    )
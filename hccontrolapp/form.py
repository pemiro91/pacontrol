import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from hccontrolapp.models import Producto, Establecimiento, Traslado, User, Material, ProductoEstablecimiento


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'imagen', 'nombre_producto', 'cantidad_existente', 'costo', 'categoria_producto', 'fecha')

        exclude = ['fecha']

        labels = {
            "Imagen": "Imagen del producto",
            "nombre_producto": "Nombre del producto",
            "cantidad_existente": "Cantidad Existente",
            "costo": "Costo (USD)",
            "categoria_producto": "Categoría de producto"
        }

        widgets = {
            'nombre_producto': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del producto',
                       'required': True}),

            'cantidad_existente': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba la cantidad existente', 'required': True}),

            'costo': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el costo', 'required': True}),

            'categoria_producto': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                               'la '
                                                                                               'categoría',
                                                      'required': True}),

        }


class TrasladoForm(forms.Form):
    class Meta:
        model = Traslado
        fields = ('producto', 'establecimiento', 'cantidad_trasladar', 'user', 'fecha')

        exclude = ['fecha', 'producto', 'user']

    establecimiento = forms.ModelChoiceField(queryset=Establecimiento.objects.all(),
                                             widget=forms.Select(attrs={'class': 'select form-control',
                                                                        'label': 'Seleccione el establecimiento',
                                                                        'required': True}))

    cantidad_trasladar = forms.CharField(label='Cantidad a trasladar',
                                         widget=forms.NumberInput(attrs={'class': 'form-control text',
                                                                         'placeholder': 'Escriba la cantidad a '
                                                                                        'trasladar',
                                                                         'required': True}))

    precio_venta = forms.CharField(label='Precio de venta (CUP)',
                                   widget=forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control text',
                                                                   'placeholder': 'Escriba el precio de la venta',
                                                                   'required': True}))


class TrasladoEstablecimientoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        establecimiento_id = kwargs.pop("establecimiento_id")
        super(TrasladoEstablecimientoForm, self).__init__(*args, **kwargs)
        self.fields['establecimiento'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'class': 'select form-control',
                                       'label': 'Seleccione el establecimiento',
                                       'required': True}),
            queryset=Establecimiento.objects.exclude(pk=establecimiento_id))

    class Meta:
        model = Traslado
        fields = ('producto', 'establecimiento', 'cantidad_trasladar', 'user', 'fecha')

        exclude = ['fecha', 'producto', 'user']

    cantidad_trasladar = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control text',
                                                                         'placeholder': 'Escriba la cantidad a '
                                                                                        'trasladar',
                                                                         'required': True}))


CHOICES_UNIDAD = [
    ('Metro', 'Metro'),
    ('Unidad', 'Unidad')
]


class MaterialForm(forms.ModelForm):
    unidad_medida = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select form-control',
                                                                 'label': 'Seleccione la unidad de medida',
                                                                 'required': True}), choices=CHOICES_UNIDAD)

    class Meta:
        model = Material
        fields = ('imagen', 'nombre_material', 'cantidad', 'costo', 'unidad_medida', 'fecha')

        exclude = ['fecha']

        labels = {
            "imagen": "Imagen del material",
            "nombre_material": "Nombre del material",
            "cantidad": "Cantidad",
            "costo": "Costo (USD)",
            "unidad_medida": "Unidad de medida"
        }

        widgets = {
            'nombre_material': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del material',
                       'required': True}),

            'cantidad': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba la cantidad', 'required': True}),

            'costo': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el costo', 'required': True}),

            'unidad_medida': forms.Select(attrs={'class': 'select form-control', 'label': 'Escriba la unidad de medida',
                                                 'required': True}),
        }


CHOICES = [
    (False, 'Masculino'),
    (True, 'Femenino')
]

CHOICES_ROL = [(True, 'Dependiente'),
               (False, 'Administrador')]


class UserForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Escriba la contraseña'}), label='Contraseña')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}), label='Confirmar contraseña')
    rol = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select form-control',
                                                       'label': 'Seleccione el rol del usuario',
                                                       'required': True}), choices=CHOICES_ROL)
    sexo = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'carnet', 'rol', 'sexo', 'username', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre', 'required': True}),

            'last_name': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba los apellidos', 'required': True}),

            'username': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el usuario', 'required': True}),

            'rol': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione el rol del usuario',
                                       'required': True}),

            'sexo': forms.RadioSelect,

            'carnet': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el carnet de identidad',
                       'required': True}),
        }

        labels = {
            "first_name": "Nombre(s)",
            "last_name": "Apellidos",
            "username": "Usuario",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
            "rol": "Rol",
            "carnet": "Carnet de identidad",
            "sexo": "Género",
        }

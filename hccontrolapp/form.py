import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from hccontrolapp.models import Producto, Establecimiento, Traslado, User


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'imagen', 'nombre_producto', 'cantidad_existente', 'costo', 'precio_venta', 'categoria_producto',
            'establecimiento', 'fecha')

        exclude = ['fecha']

        labels = {
            "Imagen": "Imagen del producto",
            "nombre_producto": "Nombre del producto",
            "cantidad_existente": "Cantidad Existente",
            "costo": "Costo",
            "precio_venta": "Precio venta",
            "categoria_producto": "Categoría de producto",
            "establecimiento": "Establecimiento",
        }

        widgets = {
            'nombre_producto': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del producto',
                       'required': True}),

            'cantidad_existente': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba la cantidad existente', 'required': True}),

            'costo': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el costo', 'required': True}),

            # 'precio_venta': forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step': "0.01"})),

            'precio_venta': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el precio de la venta', 'required': True}),

            'categoria_producto': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                               'la '
                                                                                               'categoría',
                                                      'required': True}),

            'establecimiento': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                            'el '
                                                                                            'establecimiento',
                                                   'required': True}),
            # 'precio': forms.NumberInput(
            #     attrs={'class': 'form-control ', 'placeholder': 'Escriba el precio de la pieza', })

        }


class TrasladoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        establecimiento_id = kwargs.pop("establecimiento_id")
        super(TrasladoForm, self).__init__(*args, **kwargs)
        print(establecimiento_id)
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


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'imagen', 'nombre_producto', 'cantidad_existente', 'costo', 'precio_venta', 'categoria_producto',
            'establecimiento', 'fecha')

        exclude = ['fecha']

        labels = {
            "Imagen": "Imagen del producto",
            "nombre_producto": "Nombre del producto",
            "cantidad_existente": "Cantidad Existente",
            "costo": "Costo",
            "precio_venta": "Precio venta",
            "categoria_producto": "Categoría de producto",
            "establecimiento": "Establecimiento",
        }

        widgets = {
            'nombre_producto': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del producto',
                       'required': True}),

            'cantidad_existente': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba la cantidad existente', 'required': True}),

            'costo': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el costo', 'required': True}),

            # 'precio_venta': forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step': "0.01"})),

            'precio_venta': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el precio de la venta', 'required': True}),

            'categoria_producto': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                               'la '
                                                                                               'categoría',
                                                      'required': True}),

            'establecimiento': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                            'el '
                                                                                            'establecimiento',
                                                   'required': True}),
            # 'precio': forms.NumberInput(
            #     attrs={'class': 'form-control ', 'placeholder': 'Escriba el precio de la pieza', })

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

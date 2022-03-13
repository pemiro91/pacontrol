import datetime

from django import forms

from hccontrolapp.models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'imagen', 'nombre_producto', 'cantidad_existente', 'costo', 'precio_venta', 'inversion', 'cantidad_vendida',
            'ganancia', 'cantidad_a_vender', 'categoria_producto', 'fecha')

        exclude = ['fecha']

        labels = {
            "Imagen": "Imagen del producto",
            "nombre_producto": "Nombre del producto",
            "cantidad_existente": "Cantidad Existente",
            "costo": "Costo",
            "precio_venta": "Precio venta",
            "inversion": "Inversión",
            "cantidad_vendida": "Cantidad vendida",
            "ganancia": "Ganancia",
            "cantidad_a_vender": "Cantidad a vender",
            "categoria_producto": "Categoría de producto",
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

            'inversion': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba la inversión', 'required': True}),

            'cantidad_vendida': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Cantidad vendida', 'required': True}),

            'ganancia': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Ganancia', 'required': True}),

            'cantidad_a_vender': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Cantidad a vender', 'required': True}),

            'categoria_producto': forms.Select(attrs={'class': 'select form-control', 'label': 'Seleccione '
                                                                                               'la '
                                                                                               'categoría',
                                                      'required': True}),
            # 'precio': forms.NumberInput(
            #     attrs={'class': 'form-control ', 'placeholder': 'Escriba el precio de la pieza', })

        }

import datetime

from django import forms

from hccontrolapp.models import Producto, Establecimiento, Traslado


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

from django import forms
from .models import *

from django import forms
from .models import Producto, Categoria, Subcategoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [ 'sku', 'nombre', 'descripcion', 'precio', 'stock','categoria', 'subcategoria', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 1, 'style': 'resize:none; overflow:hidden;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['subcategoria'].queryset = Subcategoria.objects.none()

        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoria_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Subcategoria queryset
        elif self.instance.pk:
            self.fields['subcategoria'].queryset = self.instance.categoria.subcategorias.order_by('nombre')

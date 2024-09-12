from django import forms
from .models import Product,Magazine,Shop,Cart

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'title', 'product_id','price','size','color']

class MagazineForm(forms.ModelForm):
    class Meta:
        model=Magazine
        fields=['pic']

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['photo1', 'photo2', 'photo3', 'name', 'product_id', 'price', 'size', 'color', 'cat','gen','design','fit','occasion','sleeve','neck','wash_care']



class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['product']
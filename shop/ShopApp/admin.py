from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from .models import *
from PIL import Image
from django.utils.safestring import mark_safe


# Register your models here.




admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Smartphone)
admin.site.register(Notebook)
admin.site.register(Headphones)
admin.site.register(Tablet)
admin.site.register(TV)
admin.site.register(Console)
admin.site.register(Order)
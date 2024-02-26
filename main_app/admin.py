from django.contrib import admin
from .models import Product, Request, List, ListProduct, Cart, CartProduct, Tag

# Register your models here.
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Request)
admin.site.register(List)
admin.site.register(ListProduct)
admin.site.register(Cart)
admin.site.register(CartProduct)


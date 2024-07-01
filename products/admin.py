from django.contrib import admin
from .models import (
    ProductsModel, OrderProductsModel, OrderModel
)

admin.site.register(ProductsModel)
admin.site.register(OrderModel)
admin.site.register(OrderProductsModel)

from django.contrib import admin
from .models import MenuPosition, MenuTable, Orders, OrderDetails


admin.site.register(MenuPosition)
admin.site.register(MenuTable)
admin.site.register(Orders)
admin.site.register(OrderDetails)
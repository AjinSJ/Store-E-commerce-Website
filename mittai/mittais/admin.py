from django.contrib import admin

# Register your models here.
from mittais.models import Movie,Order,Cart,CartItem,Category,Product,TopBrands,NewLaunch


admin.site.register(Movie)


admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(TopBrands)
admin.site.register(NewLaunch)

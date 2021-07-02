from django.contrib import admin
from .models import Station, Bike, Rental, Payment
# Register your models here.

admin.site.register(Station)
admin.site.register(Bike)
admin.site.register(Rental)
admin.site.register(Payment)

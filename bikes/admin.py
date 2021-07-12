from django.contrib import admin
from .models import Station, Bike, Rental, Payment
# Register your models here.


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'working')
    list_display_links = ('id', 'address')
    list_editable = ('working',)
    # search_fields = ('id', 'address')
    list_per_page = 25


admin.site.register(Station, StationAdmin)


class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'working', 'available')
    list_display_links = ('id', 'station')
    list_editable = ('working', 'available')
    # search_fields = ('id',  'station',)
    list_per_page = 25


admin.site.register(Bike, BikeAdmin)


class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date', 'start_station', 'end_station', 'cost', 'plan')
    list_display_links = ('id',)
    # search_fields = ('id', 'user')
    list_per_page = 25


admin.site.register(Rental, RentalAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'rental', 'status',)
    list_display_links = ('id', 'rental')
    # search_fields = ('id', 'rental', 'status')
    list_per_page = 25


admin.site.register(Payment, PaymentAdmin)

admin.site.site_header = 'Bike On Rent Admin Panel'
admin.site.site_title = 'Bike On Rent Admin'
admin.site.index_title = 'Bike On Rent Admin Panel'
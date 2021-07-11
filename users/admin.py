from django.contrib import admin
from .models import User, Profile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'address', 'balance')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email', 'phone_number', 'address')
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
from django.contrib import admin

from authorization.models import User, PhoneNumber


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'invite_code', 'create_date',)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'create_date',)


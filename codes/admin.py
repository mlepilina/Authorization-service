from django.contrib import admin

from codes.models import ConfirmationCode


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'create_date', 'last_sending_time', 'confirmation_time',)


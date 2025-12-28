from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'status')
    list_filter = ('status',)

from django.contrib import admin

from django.forms import TextInput, Textarea
# from django.db import models

from apps.telegram_bot.models import *


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('ui', 'name', 'first_ip', 'requests', 'ans_added', 'ans_got', 'subsription_lvl', 'created', 'updated')
    fields = list_display


@admin.register(Rsi)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'interval', 'period', 'infelicity', 'value', 'last_value', 'side', 'created')
    fields = list_display


@admin.register(CurrencyPair)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('service', 'name')
    fields = list_display

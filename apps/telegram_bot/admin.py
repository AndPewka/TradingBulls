from django.contrib import admin

from django.forms import TextInput, Textarea
# from django.db import models

from apps.telegram_bot.models import *


@admin.register(Client)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('login', 'email', 'password', 'password_hash', 'last_login', 'state', 'max_settings_count', 'api_parameters')


@admin.register(Service)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('title', 'api_class_name')


@admin.register(Setting)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('client', 'currency_pair', 'trading_value', 'stop_loss', 'take_profit', 'label', 'parameters')


@admin.register(Indicator)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('setting', 'kind', 'parameters')


@admin.register(CurrencyPair)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('service', 'name', 'state')


from django.contrib import admin
from .models import Category, Machine


class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, AdminCategory)


class AdminMachine(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'modified',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['modified']


admin.site.register(Machine, AdminMachine)

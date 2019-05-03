from django.contrib import admin
from .models import Request, AboutRequest
import csv
import datetime
from django.http import HttpResponse
import africastalking
import requests


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def export(modeladmin, request, queryset):
    # Initialize SDK
    username = "sandbox"
    api_key = "eebad8444bbd0e1031806a9f3a359bb288dc4a52b7968554538063fa6d157f38"
    africastalking.initialize(username, api_key)

    request_id = ""
    request_user = ""
    number = ""

    queryset.update(approved=True)
    for query in queryset:
        request_id = query.id
        request_user = query.user
        number = query.phone_number

    # Initialize a service e.g. SMS
    sms = africastalking.SMS
    response = sms.send("Hi {} , your request id {} has been approved".format(request_user, request_id), [number])
    print(response)


export.short_description = 'Approve Request'


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'address_of_delivery', 'created', 'modified', 'active', 'approved', 'paid']
    list_editable = ['active', 'approved', 'paid']
    actions = [export_to_csv, export]


admin.site.register(AboutRequest, OrderDetailsAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'price', 'product', 'quantity']
    list_filter = ['product', 'quantity', 'created']
    actions = [export_to_csv]


admin.site.register(Request, OrderItemAdmin)

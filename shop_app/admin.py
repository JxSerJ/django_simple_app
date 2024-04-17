from django.contrib import admin
from .models import Product, Client, Order, OrderDetail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'creation_date')
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')

    ordering = ('id',)

    fieldsets = (
        ('Main info', {
            'fields': ('name', 'price', 'description'),
        }),
        ('Service info', {
            'fields': ('creation_date',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('creation_date',)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    # inlines = (ProductInline,)
    empty_value_display = 'N/A'

    fieldsets = (
        ('Product info', {
            'fields': ('product', 'quantity'),
            'description': 'Use corresponding change-page',
        }),
        ('Order info', {
            'fields': ('order',),
            'description': 'Use corresponding change-page',
        }),
    )

    list_display = ('order', 'product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # inlines = (ProductInline,)
    empty_value_display = 'N/A'

    fieldsets = (
        ('Order info', {
            'fields': ('cost', 'date'),
        }),
        ('User and payment info', {
            'fields': ('paid', 'client',),
        }),
    )

    list_display = ('cost', 'date', 'paid', 'client',)
    readonly_fields = ('date', 'cost',)

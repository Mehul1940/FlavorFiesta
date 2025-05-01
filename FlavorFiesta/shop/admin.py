from django.contrib import admin
from .models import Order, OrderItem, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_price', 'total')
    fields = ('product', 'quantity', 'item_price', 'total')
    
    def item_price(self, instance):
        return instance.product.price
    item_price.short_description = "Unit Price"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'status', 'items_count')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('order_date',)
    inlines = [OrderItemInline]
    list_editable = ('status',)
    date_hierarchy = 'order_date'
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'order_date', 'status')
        }),
        ('Financial Details', {
            'fields': ('total_amount',),
            'classes': ('collapse',)
        }),
        ('Shipping Information', {
            'fields': ('shipping_address',),
            'classes': ('wide',)
        }),
    )
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total')
    list_filter = ('product',)
    search_fields = ('order__id', 'product__name')
    raw_id_fields = ('order', 'product')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'item', 'quantity', 'get_total')
    list_filter = ('item',)
    search_fields = ('session_key', 'item__name')
    raw_id_fields = ('item',)
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total'
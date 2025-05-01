from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = ('name', 'price', 'category', 'is_vegetarian', 'is_featured', 'image_preview')
    list_filter = ('is_vegetarian', 'is_featured', 'category')
    search_fields = ('name', 'description', 'ingredients')
    list_editable = ('price', 'is_vegetarian', 'is_featured')
    list_per_page = 25
    ordering = ('name',)
    
    # Form view configuration
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('Dietary Information', {
            'fields': ('is_vegetarian', 'ingredients'),
            'classes': ('collapse',)
        }),
        ('Media & Promotion', {
            'fields': ('image', 'image_preview', 'is_featured'),
            'classes': ('wide',)
        }),
    )
    readonly_fields = ('image_preview',)
    
    # Image preview method
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Preview'

    # Optional: Add validation
    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
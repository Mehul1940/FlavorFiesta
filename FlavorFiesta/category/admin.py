from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = ('name', 'slug', 'description_short')
    list_editable = ('slug',)  # Only if you want slugs editable in list view
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    ordering = ('name',)

    # Form view configuration
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    # Custom methods
    def description_short(self, obj):
        """Truncate description for list view"""
        return obj.description[:75] + '...' if obj.description else ''
    description_short.short_description = 'Description Preview'

    # Optional: Protect against accidental slug changes
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Existing object
            return ('slug',)
        return ()
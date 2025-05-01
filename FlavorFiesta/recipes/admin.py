from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = ('title', 'author', 'created_at', 'views', 'image_preview', 'description_short')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'description', 'ingredients', 'author__username')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    list_editable = ('views',)
    list_per_page = 25
    ordering = ('-created_at',)
    
    # Form view configuration
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'image', 'image_preview')
        }),
        ('Content', {
            'fields': ('description', 'ingredients', 'instructions'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at'),
            'classes': ('wide',)
        }),
    )
    readonly_fields = ('created_at', 'image_preview')
    
    # Custom methods
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def description_short(self, obj):
        return obj.description[:100] + '...' if obj.description else ''
    description_short.short_description = 'Description'
    
    # Query optimization
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
    
    # Protection for existing records
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Existing object
            return self.readonly_fields + ('author',)
        return self.readonly_fields

    # Optional: Add custom actions
    actions = ['reset_views']
    
    def reset_views(self, request, queryset):
        queryset.update(views=0)
    reset_views.short_description = "Reset views for selected recipes"
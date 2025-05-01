from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Favorite, Profile

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'added_on')
    list_filter = ('added_on', 'user')
    search_fields = ('user__username', 'recipe__title')
    raw_id_fields = ('user', 'recipe')
    date_hierarchy = 'added_on'
    ordering = ('-added_on',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'recipe')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'location', 'birth_date', 'profile_image', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Preview'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'date_joined', 'get_location')
    
    def get_location(self, obj):
        return obj.profile.location if hasattr(obj, 'profile') else ''
    get_location.short_description = 'Location'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_short', 'location', 'birth_date', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('user__username', 'bio', 'location')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('user', 'created_at')
        }),
        ('Personal Info', {
            'fields': ('bio', 'location', 'birth_date')
        }),
        ('Profile Image', {
            'fields': ('profile_image', 'image_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def bio_short(self, obj):
        return obj.bio[:50] + '...' if obj.bio else ''
    bio_short.short_description = 'Bio'
    
    def image_preview(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Preview'

# Unregister the original User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
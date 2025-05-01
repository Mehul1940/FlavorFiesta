from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('favorites/add/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-favorite/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('register/', views.register, name='register'), 
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

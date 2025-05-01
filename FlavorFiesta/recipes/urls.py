from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('popular/', views.popular_recipes, name='popular_recipes'),
    path('new/', views.new_recipes, name='new_recipes'),
    path('create/', views.create_recipe, name='create_recipe'),
]

from django.shortcuts import render, redirect , get_object_or_404
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

# All Recipes
def recipe_list(request):
    recipes = Recipe.objects.all()

    recipe_title = request.GET.get('recipe_title')
    if recipe_title !="" and recipe_title is not None:
        recipes = recipes.filter(title__icontains=recipe_title)

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.views += 1
    recipe.save()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

# Popular Recipes
def popular_recipes(request):
    popular_recipes = Recipe.objects.filter(views__gt=60).order_by('-views')[:10]
    return render(request, 'recipes/popular_recipes.html', {'popular_recipes': popular_recipes})

# New Recipes
def new_recipes(request):
    recipes = Recipe.objects.order_by('-created_at')[:10]
    return render(request, 'recipes/new_recipes.html', {'recipes': recipes})

# Submit a Recipe
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})

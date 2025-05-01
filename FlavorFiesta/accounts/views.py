from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Favorite , Profile
from .forms import ProfileForm , UserRegisterForm , AuthenticationForm
from recipes.models import Recipe
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , authenticate , logout


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile, created = Profile.objects.get_or_create(user=user)

            if created:
                profile.bio = profile_form.cleaned_data['bio']
                profile.location = profile_form.cleaned_data['location']
                profile.profile_image = profile_form.cleaned_data['profile_image']
                profile.birth_date = profile_form.cleaned_data['birth_date']
                profile.save()

            login(request, user)  
            return redirect('accounts:login')  

    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'favorites/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('food:index')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'favorites/login.html', {'form': form,'page': 'login'})

def user_logout(request):
    logout(request) 
    return redirect('food:index')  

# Show all favorite recipes for the logged-in user
@login_required
def favorite_recipes(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})

# Add a recipe to favorites
@login_required
def add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the recipe is already in the user's favorites
    if not Favorite.objects.filter(user=request.user, recipe=recipe).exists():
        Favorite.objects.create(user=request.user, recipe=recipe)
    
    return redirect('favorites:favorite_recipes')

@login_required
@require_POST
def remove_from_favorites(request, recipe_id):
    Favorite.objects.filter(user=request.user, recipe_id=recipe_id).delete()
    return redirect('accounts:favorite_recipes')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  # Change name if you name the URL differently
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'favorites/profile.html', {'form': form})
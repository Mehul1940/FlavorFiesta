from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Item
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator

def index(request):
    food_list = Item.objects.all()

    food_name = request.GET.get('food_name')
    if food_name != '' and food_name is not None:
        food_list = food_list.filter(name__icontains=food_name)

    paginator = Paginator(food_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    context = {
        'foods': page_obj  
    }
    return render(request, 'food/index.html', context)

def about(request):
    return render(request, 'food/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Message from {name} <{email}>:\n\n{message}"

        try:
            send_mail(
                subject='New Contact Form Submission',
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],  # set in settings.py
                fail_silently=False,
            )
            messages.success(request, "Thank you for reaching out. Your message has been sent!")
        except Exception as e:
            messages.error(request, "Sorry, we couldn't send your message. Please try again later.")
    return render(request, 'food/contact.html')

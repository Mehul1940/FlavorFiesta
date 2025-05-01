# python -m venv venv  - First Create a Virtual Environment

# venv\Scripts\activate - Then Activate The Environment

# pip install django - Install django in Environment

# django-admin startproject Project_Name - For creating a project in django

# cd Project_Name - For going inside the project

# python manage.py runserver - For Running your django Project

# python manage.py startapp App_Name - For creating an App in django

# Now create a Class in models.py 

# After The Creation Create table by using 
-> python manage.py makemigration 
-> python manage.py migrate

# Create media in your main project and apply  This in your settings.py
-> MEDIA_URL = '/media/'
-> MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# And For Css Create in your main project and apply  This in your settings.py
-> STATIC_URL = '/static/'
-> STATICFILES_DIRS = [
    BASE_DIR / "static",
]
-> STATIC_ROOT = BASE_DIR / "staticfiles"

# After That Create a Template And In That Template Create a Folder Where you put Your Html files and a base.html file for minimizing code
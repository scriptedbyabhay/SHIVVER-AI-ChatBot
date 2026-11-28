from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('api/chat/', views.chat_api, name = 'chat_api'),
]

# urlpatterns is a list of URL patterns
# The empty string '' represents the root URL
# For example
    # http://127.0.0.1:8000/

# When someone visits this address, Django executes 'views.home' i.e. the home() function from views.py
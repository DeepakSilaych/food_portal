from django.urls import path
from .views import sso_login, sso_redirect, logout_view, add_food, view_bookings

urlpatterns = [
    path('login/', sso_login, name='login'),
    path('redirect/', sso_redirect, name='sso_redirect'),
    path('logout/', logout_view, name='logout'),
    path('', add_food, name='add_food'),
    path('food-success/', add_food, name='food_success'),
    path('view/', view_bookings, name='view_bookings'),
]

import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import FoodBooking, FoodOrder
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum

# SSO Authentication function
def sso_login(request):
    project_id = '051086d5-4401-4dc8-9e31-90cd97fccd38'
    sso_url = f"https://sso.tech-iitb.org/project/{project_id}/ssocall/"
    return redirect(sso_url)

def sso_redirect(request):
    token = request.GET.get('accessid')
    response = requests.post(
        'https://sso.tech-iitb.org/project/getuserdata',
        data={'id': token}
    )

    if response.status_code == 200:
        user_data = response.json()
        user, created = User.objects.get_or_create(
            username=user_data['roll'],
        )
        login(request, user)
        return redirect('add_food')
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('add_food')

def add_food(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        ps = request.POST.get('select_ps')
        food_items = request.POST.getlist('food_item')
        quantities = request.POST.getlist('quantity')
        
        if food_items and quantities:
            booking = FoodBooking.objects.create(user=request.user, select_ps=ps)

            for food_item, quantity in zip(food_items, quantities):
                if food_item and quantity:
                    FoodOrder.objects.create(booking=booking, food_item=food_item, quantity=int(quantity))

            return redirect('food_success')
    
    return render(request, 'add_food.html', {
        'food_choices': FoodOrder.FOOD_CHOICES,
        'ps_choices': FoodBooking._meta.get_field('select_ps').choices,
    })

def food_success(request):
    logout(request)
    return render(request, 'food_success.html')



@staff_member_required
def view_bookings(request):
    start_time = request.GET.get('start')
    end_time = request.GET.get('end')

    if start_time and end_time:
        bookings = FoodBooking.objects.filter(
            booked_at__range=[start_time, end_time]
        )
    else:
        bookings = FoodBooking.objects.all()

    # Aggregate the total count of each food item
    food_summary = FoodOrder.objects.values('food_item').annotate(total_quantity=Sum('quantity'))

    return render(request, 'admin_view.html', {
        'bookings': bookings,
        'food_summary': food_summary
    })

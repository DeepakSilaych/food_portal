import os
from django.db import models
from django.contrib.auth.models import User

class FoodBooking(models.Model):
    PS_CHOICES = [
        (ps, ps) for ps in os.environ.get('PS_CHOICES', 'Ideaforge,Zelta,Pathway,ISRO').split(',')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    select_ps = models.CharField(max_length=50, choices=PS_CHOICES)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.booked_at}"

class FoodOrder(models.Model):
    FOOD_CHOICES = [
        (food, food) for food in os.environ.get('FOOD_CHOICES', 'Pizza,Burger,Salad,Pasta').split(',')
    ]

    booking = models.ForeignKey(FoodBooking, related_name='orders', on_delete=models.CASCADE)
    food_item = models.CharField(max_length=50, choices=FOOD_CHOICES)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.food_item} x {self.quantity}"

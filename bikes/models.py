from django.db import models
from users.models import User
# Create your models here
# Route
# user-> station-> bike -> rental-> payment


class Station(models.Model):
    address = models.CharField(max_length=200)
    working = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.address


class Bike(models.Model):
    station = models.ForeignKey(Station, null=True, blank=True, on_delete=models.SET_NULL)
    working = models.BooleanField(default=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # bike = models.ForeignKey(bike, related_name='bike', on_delete=models.CASCADE,default="")
    bike = models.ManyToManyField(Bike, related_name='bike')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, default=None)
    start_station = models.ForeignKey(Station, related_name="start_station", on_delete=models.CASCADE)
    end_station = models.ForeignKey(Station, null=True, related_name="end_station", on_delete=models.CASCADE)
    cost = models.IntegerField(null=True)
    plan = models.TextField(default="")

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name='rental', on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return str(self.id)




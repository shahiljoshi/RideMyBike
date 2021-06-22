from django.db import models

# Create your models here


class station(models.Model):
    address = models.CharField(max_length=200)
    capacity = models.IntegerField()
    working = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.address

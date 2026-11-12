from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    cuisine = models.CharField(max_length=100)
    price_range = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    opening_time = models.CharField(max_length=50)
    closing_time = models.CharField(max_length=50)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    movie_title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100)
    seats = models.IntegerField()
    show_time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_name} - {self.movie_title}"
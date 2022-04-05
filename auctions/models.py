from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return f'{self.name}'


class Listing(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', null=True)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=7, decimal_places=2)
    picture = models.URLField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {self.category} - Starting Price: ${self.starting_price} - Active: {self.active}'


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', null=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Listing: {self.listing} - Value: {self.value}'


class Watchlist(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    item = ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'User: {self.user}, item: {self.item}'


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return humanize.naturaltime(self.timestamp)

    def __str__(self):
        return f'Listing: {self.listing.title} - User: {self.user.username} - Content: {self.content} - Timestamp: {self.timestamp}'
from datetime import timedelta

from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/')

def __str__(self):
        return self.title



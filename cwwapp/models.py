from django.db import models
from datetime import datetime


class Author(models.Model):
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Story(models.Model):
    categories = (
        ('pol', "politics"),
        ('art', "art news"),
        ('tech', "technology new"),
        ('trivia', 'trivial news'),)
    area = (
        ('uk', "uk news"),
        ('eu', "European news"),
        ('w', "world new"),)

    id = models.BigAutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=32, choices=categories, default=None)
    region = models.CharField(max_length=32, choices=area, default=None)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=512)

    def __str__(self):
        return self.headline

    def to_json(self):
        json = {
            'key': self.id,
            'headline': self.headline,
            'story_cat': self.category,
            'story_region': self.region,
            'author': self.author.username,
            'story_date': datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S"),
            'story_details': self.details,
        }
        return json

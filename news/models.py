from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.
class User(AbstractUser):
    pass


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="users_bookmarked_article")
    title = models.CharField(max_length=100)
    card_description = models.CharField(max_length=100)
    image_url = models.URLField()
    article_url = models.URLField()

    def __str__(self) -> str:
        return f"{self.user} bookmarked: {self.title}"

    def serialize(self):
        return {
            "urlToImage": self.image_url,
            "title": self.title,
            "description": self.card_description,
            "url": self.article_url
        }
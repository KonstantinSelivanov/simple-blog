from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Data model for blog posts
# Модель данных для постов блога
class Post(models.Model):
    # Post status
    # Статус постов
    STATUS_CHOICES = ( ('draft', 'Черновик'), ('published','Опубликовано') )
    # Post title
    # Заголовок постов блога
    title = models.CharField(max_length=250) 
    # Semantic URL for posts 
    # Семантический URL  для постов
    slug = models.SlugField(max_length=250, unique_for_date='published')
    # Foreign key of the author post
    # Внешний ключ автора поста
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
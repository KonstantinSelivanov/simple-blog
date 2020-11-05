from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Data model for blog posts
# Модель данных для постов блога
class Post(models.Model):
    # Post status tuple
    # Кортеж статус постов
    STATUS_CHOICES = (('draft', 'Черновик'), ('published', 'Опубликовано'))
    # Post title
    # Заголовок постов блога
    title = models.CharField(max_length=250)
    # Semantic URL for posts
    # Семантический URL  для постов
    slug = models.SlugField(max_length=250, unique_for_date='published')
    # Foreign key of the author post
    # Внешний ключ автора поста
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    # The content of the post
    # Содержание поста
    body = models.TextField()
    # Post publication date
    # Дата публикации поста
    publish = models.DateTimeField(default=timezone.now)
    # Post creation date
    # Дата создания поста
    created = models.DateTimeField(auto_now_add=True)
    # Date and time when the post was updated
    # Дата и время когда был обновлен пост
    updated = models.DateTimeField(auto_now=True)
    # Post status
    # Статус поста
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    # Metadata. Sort order of posts in descending order of publication date
    # Метаданные. Порядок сортировки постов по убыванию даты публикации
    class Meta:
        ordering = ('-publish',)

    # The method returns the display of the object in an understandable way
    # Метод возвращает отображение объекта понятном виде
    def __str__(self):
        return self.title

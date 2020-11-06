from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Data model for blog posts
# Модель данных для ствтей блога
class Post(models.Model):
    # Post status tuple
    # Кортеж статус статей
    STATUS_CHOICES = (('draft', 'Черновик'), ('published', 'Опубликовано'))
    # Post title
    # Заголовок статьи блога
    title = models.CharField(verbose_name='Заголовок', max_length=250)
    # Semantic URL for posts
    # Семантический URL  для статьи
    slug = models.SlugField('URL', max_length=250, unique_for_date='published')
    # Foreign key of the author post
    # Внешний ключ автора статьи
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='blog_posts')
    # The content of the post
    # Содержание статьи
    body = models.TextField(verbose_name='Содержание статьи')
    # Post publication date
    # Дата публикации статьи
    publish = models.DateTimeField('Дата публикации статьи', default=timezone.now)
    # Post creation date
    # Дата создания статьи
    created = models.DateTimeField(auto_now_add=True)
    # Date and time when the post was updated
    # Дата и время когда была обновлена статья
    updated = models.DateTimeField(auto_now=True)
    # Post status
    # Статус статьи
    status = models.CharField(verbose_name='Статус',
        max_length=10, choices=STATUS_CHOICES, default='draft')

    # Metadata. Sort order of posts in descending order of publication date
    # Метаданные. Порядок сортировки постов по убыванию даты публикации
    class Meta:
        ordering = ('-publish',)
        verbose_name = 'статью'
        verbose_name_plural = 'Статьи'

    # The method returns the display of the object in an understandable way
    # Метод возвращает отображение объекта понятном виде
    def __str__(self):
        return self.title

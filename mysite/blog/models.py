from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Manager model
# Менеджер модели
class PublishedManager(models.Manager):
    # Method return QuerySet with filter on "status"
    # Метод возврата QuerySet с фильтром по "status"
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

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
    slug = models.SlugField('URL', max_length=250, unique_for_date='date_published')
    # Foreign key of the author post
    # Внешний ключ автора статьи
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='blog_posts')
    # Preview post
    # Предварительный просмотр статьи
    body_preview = models.TextField(verbose_name='Предварительный просмотр статьи')
    # The content of the post
    # Содержание статьи
    body = models.TextField(verbose_name='Содержание статьи')
    # Post publication date
    # Дата публикации статьи
    date_published = models.DateTimeField('Дата публикации статьи', default=timezone.now)
    # Post creation date
    # Дата создания статьи
    created = models.DateTimeField('Дата создания статьи', auto_now_add=True)
    # Date and time when the post was updated
    # Дата и время когда была обновлена статья
    updated = models.DateTimeField(auto_now=True)
    # Post status
    # Статус статьи
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    # Metadata. Sort order of posts in descending order of publication date
    # Метаданные. Порядок сортировки постов по убыванию даты публикации
    
    # The default model manager
    # Менеджер модели по умолчанию
    objects = models.Manager()
    # New model manager
    # Новый менеджер модели
    published = PublishedManager()

    class Meta:
        ordering = ('-date_published',)
        verbose_name = 'статью'
        verbose_name_plural = 'Статьи'

    # The method returns the display of the object in an understandable way
    # Метод возвращает отображение объекта понятном виде
    def __str__(self):
        return self.title
    
    # Getting the URL of the link to the post
    # Получение URL ссылки на пост
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.date_published.year, self.date_published.month, self.date_published.day, self.slug])



from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Manager model
# Менеджер модели
class PublishedManager(models.Manager):
    # Method return QuerySet with filter on "status"
    # Метод возврата QuerySet с фильтром по "status"
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

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
    slug = models.SlugField(verbose_name='URL', max_length=250, unique_for_date='date_published')
    # Foreign key of the author post
    # Внешний ключ автора статьи
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='blog_posts')
    # The content of the post
    # Содержание статьи
    body = models.TextField(verbose_name='Содержание статьи')
    # Post publication date
    # Дата публикации статьи
    date_published = models.DateTimeField('Дата публикации статьи', default=timezone.now)
    # Post creation date
    # Дата создания статьи
    created = models.DateTimeField(verbose_name='Дата создания статьи', auto_now_add=True)
    # Date and time when the post was updated
    # Дата и время когда была обновлена статья
    updated = models.DateTimeField(auto_now=True)
    # Post status
    # Статус статьи
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
     # The default model manager
    # Менеджер модели по умолчанию
    objects = models.Manager()
    # New model manager
    # Новый менеджер модели
    published = PublishedManager()
    # Manager tags 
    # Менеджер тегов
    tags = TaggableManager()



    # Metadata. Sort order of posts in descending order of publication date
    # Метаданные. Порядок сортировки постов по убыванию даты публикации
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
        #pylint: disable=E1101
        return reverse('blog:post_detail', args=[self.date_published.year, self.date_published.month, self.date_published.day, self.slug])

# Comment model
# Модель комментариев
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(verbose_name='Имя', max_length=80)
    email = models.EmailField(verbose_name='e-mail')
    # The content of the comment
    # Содержание комментария
    body = models.TextField(verbose_name='Комментарий')
    # Comment creation date
    # Дата создания комментария
    created = models.DateTimeField(verbose_name='Дата создания комментария',auto_now_add=True)
    # Date and time when the comment was updated
    # Дата и время когда был обновлен комментарий
    updated = models.DateTimeField(verbose_name='Дата изменения комментария', auto_now=True)
    # 
    # 
    moderation = models.BooleanField(verbose_name='Модерация', default=True)

    # Metadata. Sort order of comments in descending order of publication date
    # Метаданные. Порядок сортировки комментариев по убыванию даты публикации
    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    # The method returns the display of the object in an understandable way
    # Метод возвращает отображение объекта понятном виде
    def __str__(self):
        return 'Комментарий от {} на {}'.format(self.name, self.post)
    

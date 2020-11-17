from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Registration of a decareable class Post
    Регистрация декарируемого класса Post

    """

    # The fields that models will designate on the list page
    # Поля модели которые будут отображаться на странице списка
    list_display = ('title', 'slug', 'author', 'date_published', 'status')
    # Filtering the posts list
    # Фильтрация списка статей
    list_filter = ('status', 'created', 'date_published', 'author')
    # Search
    # Поиск
    search_fields = ('title', 'body')
    # Automatic URL generation (slug)
    # Автоматическая генерация URL (slug)
    prepopulated_fields = {'slug': ('title',)}
    # Navigation by post date
    # Навигация по датам публикации
    date_hierarchy = 'date_published'
    # Sort posts by 'status', 'date_published'
    # Сортировка статей по 'status', 'date_published'
    ordering = ('status', 'date_published')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Registration of a decareable class Comment
    Регистрация декарируемого класса Comment

    """

    # The fields that models will designate on the list page
    # Поля модели которые будут отображаться на странице списка
    list_display = ('name', 'email', 'post', 'created', 'moderation')
    # Filtering the comment list
    # Фильтрация списка комментариев
    list_filter = ('moderation', 'created', 'updated')
    # Search
    # Поиск
    search_fields = ('name', 'email', 'body')

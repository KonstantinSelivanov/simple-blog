from django.contrib import admin
from .models import Post


# Registration of a decareable class Post
# Регистрация декарируемого класса Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # The fields that models will designate on the list page
    # Поля модели которые будут отображаться на странице списка
    list_display = ('title', 'slug', 'author', 'date_published', 'status')
    # Filtering the post list
    # Фильтрация списка статей
    list_filter = ('status', 'created', 'date_published', 'author')
    # Search
    # Поиск
    search_fields = ('title', 'body_preview', 'body')
    # Automatic URL generation (slug)
    # Автоматическая генерация URL (slug)
    preopopulated_fields = {'slug': ('title',)}
    # Navigation by post date
    # Навигация по датам публикации 
    date_hierarchy = 'date_published'
    # Sort posts by 'status', 'date_published'
    # Сортировка статей по 'status', 'date_published'
    ordering = ('status', 'date_published')

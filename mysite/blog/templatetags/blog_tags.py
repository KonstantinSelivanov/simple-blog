from django import template
from ..models import Post


# A module-level variable named register, which is an instance 
# of template.Library in which all tags and filters are registered.
# Переменна уровня модуля с именем register, которая является экземпляром 
# template.Library, в котором зарегистрированы все теги и фильтры.
register = template.Library()

# Decorator for registering a new tag
# Декоратор для регистрации нового тега
@register.simple_tag(name='total_posts')
# The 'total_posts' tag returns the number of posted posts
# Тег 'total_posts' возвращает количество опубликованных статей
def total_posts():
    return Post.published.count()
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

# Decorator for using an inclusive tag
# Декоратор для использования инклюзивного тега
@register.inclusion_tag('blog/post/latest_posts.html')
# Display tag for recent blog posts
# Тег отображения последних статей блога
def show_latest_posts(count=5):
    # Sorting the result by the date of publication of the posts. 
    # Limit the selection to the number of posts that we want to display in 
    # the list of recently published posts [: count]
    # Сортировка результата по дате публикации статей. 
    # Ограничить выборку тем количеством статей, которое мы хотим отображать 
    # в списке последних опубликованных статей [:count]
    latest_posts = Post.published.order_by('-date_published')[:count]
    return {'latest_posts': latest_posts}

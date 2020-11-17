from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from ..models import Post


# A module-level variable named register, which is an instance
# of template.Library in which all tags and filters are registered.
# Переменна уровня модуля с именем register, которая является экземпляром
# template.Library, в котором зарегистрированы все теги и фильтры.
register = template.Library()


# Decorator for registering a new tag
# Декоратор для регистрации нового тега
@register.simple_tag(name='total_posts')
def total_posts():
    """
    The 'total_posts' tag returns the number of posted posts
    Тег 'total_posts' возвращает количество опубликованных статей
    """
    return Post.published.count()


# Decorator for registering a new tag
# Декоратор для регистрации нового тега
@register.simple_tag(name='get_most_commmented_posts')
def get_most_commmented_posts(count=5):
    """
    Simple template tag for displaying posts with the most comments.
    The annotate () method is used to add the number of comments
    to each article. Sorting the result by the number of comments.
    Limit the selection to the number of posts that we want to display in
    the list of recently published posts [: count]
    Простой шаблонный тег для отображения статей с наибольшим количеством
    комментариев. Метод annotate() служит для добавления к каждой статье
    количества ее комментариев. Сортировка результата по количеству
    комментариев. Ограничить выборку тем количеством статей, которое мы хотим
    отображать в списке последних опубликованных статей [:count]

    """

    return Post.published.annotate(total_comments=Count('comments')).\
        order_by('-total_comments')[:count]


# Decorator for using an inclusive tag
# Декоратор для использования инклюзивного тега
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Display tag for recent blog posts
    Тег отображения последних статей блога
    """
    # Sorting the result by the date of publication of the posts.
    # Limit the selection to the number of posts that we want to display in
    # the list of recently published posts [: count]
    # Сортировка результата по дате публикации статей.
    # Ограничить выборку тем количеством статей, которое мы хотим отображать
    # в списке последних опубликованных статей [:count]
    latest_posts = Post.published.order_by('-date_published')[:count]
    return {'latest_posts': latest_posts}


# Decorator for using Markdown formatting
# Декоратор для использования форматирования Markdown
@register.filter(name='markdown_format')
def markdown_format(text):
    """[summary]
    Custom template filter using Markdown formatting.
    Filter result text as HTML code
    Собственный шаблонный фильтр с помощью форматирования Markdown.
    Результат работы фильтра текст как HTML-код

    """

    return mark_safe(markdown(text))

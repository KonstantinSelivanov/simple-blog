from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# The post_list handler queries the database for all published posts using the "published" model manager
# Обработчик post_list запрашивает из базы данных все опубликованные статей с помощью менеджера моделей "published"
def post_list(request):
    # Object list 
    # Список объектов
    object_list = Post.published.all()
    # 3 posts on each page
    # 3 статьи на каждой странице
    paginator = Paginator(object_list, 3)
    # Getting the current page using a GET request
    # Получение текущей страницы с помощью GET запроса 
    page = request.GET.get('page')

    try:
        # Get a list of objects on the desired page
        # Получаем список объектов на нужной странице
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, return the first page
        # Если страница не является целым числом, возвращаем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # If the page number is greater than the total number of pages, the last page is returned
        # Если номер страницы больше, чем общее количество страниц, возвращается последння страница
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts} )

# Handler for displaying the post page
# Обработчик для отображения страницы статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             date_published__year=year, date_published__month=month, date_published__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

# Class handler analog of the "post_list" function
# Обработчик-классов аналог функции "post_list"
class PostListView(ListView):
    # Object QuerySet 
    # Список объектов
    queryset = Post.published.all()
    # 
    # 
    context_object_name = 'posts'
    # 
    # 
    paginate_py = 3
    #
    # 
    template_name = 'blog/post/list.html'
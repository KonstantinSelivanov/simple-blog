from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm


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
    # List of active comments for the current post
    # Список активных комментариев для текущей статьи
    comments = post.comments.filter(moderation=True)
    # Variable for new comments
    # Переменная для новых комментариев
    new_comment = None
    if request.method == 'POST':
        # User posted a comment. Initializing the form on a GET request
        # Пользователь отправил комментарий. Инициализируем форму при GET-запросе
        comment_form = CommentForm(data=request.POST)
        # If we receive a POST request, then fill out the form with data from the request and validate it using the is_valid () method
        # Если получаем POST-запрос, то заполняем форму данными из запроса и валидируем методом is_valid()
        if comment_form.is_valid():
            # Create a new comment, but not save to the database
            # Создание нового комментария, но не сохранение в базе данных
            new_comment = comment_form.save(commit=False)
            # Linking a comment to the current post
            # Привязка комментария к текущей статье 
            new_comment.post = post
            # Saving a comment in the database
            # Сохранение комментария в базе данных
            new_comment.save()
    else:
        # If the form is filled out incorrectly, the HTML template with error messages is displayed
        # Если форма заполнена некорректно отображается HTML-шаблон с сообщениями об ошибках
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

# Class handler analog of the "post_list" function
# Обработчик-классов аналог функции "post_list"
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_py = 3
    template_name = 'blog/post/list.html'
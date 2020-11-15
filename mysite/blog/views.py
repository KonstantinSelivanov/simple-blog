from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count
from .models import Post, Comment
from .forms import CommentForm
from taggit.models import Tag

from django.db.models import Q


# The post_list handler queries the database for all published posts using the "published" model manager
# Обработчик post_list запрашивает из базы данных все опубликованные статей с помощью менеджера моделей "published"
def post_list(request, tag_slug=None):
    #search
    # 
    search_query = request.GET.get('search1', '')

    if search_query:
        object_list = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        # Object list 
        # Список объектов
        object_list = Post.objects.all()

    # Variable for new tag
    # Переменная для новых тегов 
    tag = None
    
    # tag_slug will be set in the URL
    # tag_slug будет задаваться в URL’е 
    if tag_slug:  
        # Creation of QuerySet. Find all published articles and, if a tag slug is specified, get the corresponding Tag model object using the method get_object_or_404() 
        # Создание QuerySet. Находим все опубликованные статьи и, если указан слаг тега, получаем соответствующий объект модели Tag с помощью метода get_object_or_404()
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filtering the list of articles and leaving only those related to the received tag
        # Фильтрация списка статей и оставляем только те которые связаны с полученным тегом
        object_list = object_list.filter(tags__in=[tag])

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

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag} )

# Handler for displaying the post page
# Обработчик для отображения страницы статьи
def post_detail(request, year, month, day, post):
    # Getting a post by ID
    # Получение статьи по идентификатору
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

    # Formation of a list of related posts by tags
    # Формирование списка похожих статей по тегам
    
    # Getting all the current post ID tags. Getting a flat list - flat=True 
    # Получение всех ID тегов текущей статьи. Получение плоского списка - flat=True 
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Getting all the stations that are associated with at least one tag, excluding the current post.
    # Получение всех статьей, которые связаны хотя бы с одним тегом, исключая текущую статью. 
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Sort the result by the number of tag matches.
    # If two or more posts have the same set of tags, choose the one that is the newest.
    # Limit the selection to the number of posts that we want to display in the featured list. [:4]
    # Сортировка результата по количеству совпадений тегов. 
    # Если две и более статьи имеют одинаковый набор тегов, выбирать ту из них, которая является самой новой. 
    # Ограничить выборку тем количеством статей, которое мы хотим отображать в списке рекомендуемых. [:4]
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_published')[:4]

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})

# Class handler analog of the "post_list" function
# Обработчик-классов аналог функции "post_list"
class PostListView(ListView):
    # Using the overridden QuerySet model instead of getting all objects.
    # Использование переопределенного QuerySet модели вместо получения всех объектов.
    queryset = Post.published.all()
    # Using "posts" as an HTML template context variable that will hold the list of objects.
    # Использование "posts" в качестве переменной контекста HTML-шаблона, в которой будет храниться список объектов.
    context_object_name = 'posts'
    # Displaying three objects per page
    # Постраничное отображение по три объекта на странице
    paginate_py = 3
    # Using the specified template to form the page
    # Использование указанный шаблон для формирования страницы
    template_name = 'blog/post/list.html'
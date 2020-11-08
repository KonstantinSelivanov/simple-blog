from django.shortcuts import render, get_object_or_404
from .models import Post


# The post_list handler queries the database for all published posts using the "published" model manager
# Обработчик post_list запрашивает из базы данных все опубликованные статей с помощью менеджера моделей "published"
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts}
                  )

# Handler for displaying the post page
# Обработчик для отображения страницы статьи


def post_detail(request, post, year, month, day):
    post = get_object_or_404(Post, slug=post, status='published',
                             date_publish__year=year, date_published__month=month, date_publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

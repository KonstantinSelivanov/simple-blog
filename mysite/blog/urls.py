from django.urls import path
from . import views
from .feeds import LatestPostFeed


app_name = 'blog'

#
# 
urlpatterns = [
    # The template is matched against the "post_list" handler
    # Шаблон сопоставляется с обработчиком "post_list "
    path('', views.post_list, name='post_list'),

    # Class handler analog of the "post_list" function
    # Обработчик-классов аналог функции "post_list"
    # path('', views.PostListView.as_view(), name='post_list'),

    # The template calls the "post_detail" function
    # Шаблон вызывает функцию "post_detail"
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, 
                                                          name='post_detail'),
    
    # Template for referring to the list of articles associated with a specific tag
    # Шаблон для обращения к списку статей связанных с определенным тегом
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # Template for RSS
    # Шаблон для RSS
    path('feed/', LatestPostFeed(), name='post_feed'),
]
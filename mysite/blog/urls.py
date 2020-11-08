from django.urls import path
from . import views


app_name = 'blog'

#
# 
urlpatterns = [
    # The template is matched against the "post_list" handler
    # Шаблон сопоставляется с обработчиком "post_list "
    path('', views.post_list, name='post_list'),
    # The template calls the "post_detail" function
    # Шаблон вызывает функцию "post_detail"
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]
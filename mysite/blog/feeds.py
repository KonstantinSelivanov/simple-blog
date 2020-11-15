from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


# RSS for lastest posts
# RSS для последних статей
class LatestPostFeed(Feed):
    title = 'Мой блог'
    link = '/'
    description = 'Новые статьи в моем блоге' 

    # Receive objects that will be included in the mailing list. 
    # Only the last 5 published posts are taken
    # Получаем объекты которые будут включены в рассылку. 
    # Беруться только последние 5 опубликованных статей
    def items(self):
        return Post.published.all()[:5]
    
    # Get the title for each object from the result
    # Получаем для каждого объекта из результата заголовок
    def item_title(self, item):
        return item.title
    
    # Get a description for each object from the result, limiting it to 30 words
    # Получаем для каждого объекта из результата описание ограничив его 30 словами
    def item_description(self, item):
        return truncatewords(item.body, 30)
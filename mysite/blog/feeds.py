from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    """[summary]
    RSS for lastest posts
    RSS для последних статей

    """

    title = 'Мой блог'
    link = '/'
    description = 'Новые статьи в моем блоге'

    def items(self):
        """[summary]
        Receive objects that will be included in the mailing list.
        Only the last 5 published posts are taken
        Получаем объекты которые будут включены в рассылку.
        Беруться только последние 5 опубликованных статей

        """

        return Post.published.all()[:5]

    def item_title(self, item):
        """[summary]
        Get the title for each object from the result
        Получаем для каждого объекта из результата заголовок

        """

        return item.title

    def item_description(self, item):
        """
        Get a description for each object from the result,
        limiting it to 30 words.
        Получаем для каждого объекта из результата описание
        ограничив его 30 словами

        """

        return truncatewords(item.body, 30)

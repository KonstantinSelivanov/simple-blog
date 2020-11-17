from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """
    Sitemap object
    Объект карты сайта

    """

    # Change Frequency posts pages
    # Частота  обновления страниц статей
    changefreq = 'weekly'
    # The degree of coincidence of posts with the site topic (maximum value -1)
    # Степень совпадения статей с тематикой сайта (максимальное значение – 1)
    priority = 0.9

    def items(self):
        """
        The items () method returns a QuerySet of objects
        that will be displayed in the sitemap.
        Метод items() возвращает QuerySet объектов,
        которые будут отобра­жаться в карте сайта

        """

        return Post.published.all()

    def lastmod(self, obj):
        """
        The lastmod () method takes each object from the result of the items()
        call and returns the time the post was last modified.
        Метод lastmod() принимает каждый объект из результата вызова items()
        и возвращает время последней модификации статьи

        """

        return obj.updated

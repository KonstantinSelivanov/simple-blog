from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Comment form
    Форма комментариев

    """

    class Meta:
        """
        Name of the model based on which the form will be created
        Имя модели на основе которой будет создана форма

        """

        model = Comment
        # Form fields
        # Поля формы
        fields = ('name', 'email', 'body')

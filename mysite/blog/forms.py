from django import forms   
from .models import Comment


# Comment form
# Форма комментариев
class CommentForm(forms.ModelForm): 
    class Meta:
        # Name of the model based on which the form will be created
        # Имя модели на основе которой будет создана форма
        model = Comment
        # Form fields
        # Поля формы
        fields = ('name', 'email', 'body')

from django import forms   
from .models import Comment


# Comment form
# Форма комментариев
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

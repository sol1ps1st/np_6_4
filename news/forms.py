from django.forms import (
    ModelForm,
)

from news.models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Не выбран"

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categories']

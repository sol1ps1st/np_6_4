from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

from news.models import Post, Category


# class PostForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['author'].empty_label = "Не выбран"
#
#     class Meta:
#         model = Post
#         fields = ['title', 'text', 'author', 'categories']


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Не выбран"
        self.fields['title'].widget = forms.TextInput(attrs={'size': '60'})
        self.fields['text'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 10})
        self.fields['categories'] = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            label=Post._meta.get_field('categories').verbose_name,
        )

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categories']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

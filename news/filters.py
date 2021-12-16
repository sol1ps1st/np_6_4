from django import forms
import django_filters
from django_filters import FilterSet
from .models import (
    Post,
    Category,
)


class NewsFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    author = django_filters.AllValuesFilter(
        field_name='author__user__username',
        lookup_expr='exact',
        label='Автор',
        empty_label='Не выбран'
    )
    created = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Не ранее',
        input_formats=['%d.%m.%Y']
    )
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категория:',
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created']

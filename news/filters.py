from django import forms
from django.utils.translation import gettext_lazy as _
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
        label=_('Title')
    )
    author = django_filters.AllValuesFilter(
        field_name='author__user__username',
        lookup_expr='exact',
        label=_('Author'),
        empty_label=_('Not selected')
    )
    created = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label=_('Not earlier'),
        input_formats=['%d.%m.%Y']
    )
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label=_('Category:'),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created']

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)

from news.models import Post
from news.filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    context_object_name = "news"
    template_name = "news/news.html"
    paginate_by = 10
    queryset = Post.objects.order_by("pk")

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        qs = self.get_filter().qs
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter

        filter_params = ""
        for f_name in [str(k) for k in filter.filters]:
            if f_name in filter.data:
                filter_params += f"&{f_name}={filter.data[f_name]}"
        context['filter_params'] = filter_params

        # context['get_dict'] = {
        #     k: value[0] for k, value in dict(self.request.GET.copy()).items() if k != 'page'
        # }  # Нужно для пагинации по отфильтрованным результатам: фильтры передаются в GET словарике
        return context


class NewsPostDetail(DetailView):
    model = Post
    context_object_name = "news_post"
    template_name = "news/news_post.html"


class NewsPostDelete(DeleteView):
    model = Post
    context_object_name = "news_post"
    template_name = "news/news_delete.html"
    success_url = reverse_lazy('post_list')


class NewsPostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = "news/news_create.html"


class NewsPostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "news/news_create.html"

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

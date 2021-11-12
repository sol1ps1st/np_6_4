from django.views.generic import (
    ListView,
    DetailView,
)

from news.models import Post


class NewsList(ListView):
    model = Post
    context_object_name = "news"
    template_name = "news/news.html"
    queryset = Post.objects.order_by("-created")


class NewsPostDetail(DetailView):
    model = Post
    context_object_name = "news_post"
    template_name = "news/news_post.html"

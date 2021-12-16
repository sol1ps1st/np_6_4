from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
)
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
# from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)

from django.contrib.auth.models import User
from news.models import Post, Category
from news.filters import NewsFilter
from .forms import PostForm
from np_6_4.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=Post.categories.through)
def notify_users_new_post(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        users_mails = set()
        for c in Category.objects.filter(id__in=pk_set):
            for u in c.subscribers.all():
                if u.email:
                    users_mails.add(u.email)
        html_content = render_to_string(
            'news/email_posts.html',
            {
                'posts': [instance],
            }
        )
        msg = EmailMultiAlternatives(
            subject='Добавлена новость',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=list(users_mails)
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # send_mail(
        #     subject='Добавлена новость',
        #     message=f'Краткое содержание: {instance.text[:50]}',
        #     from_email='alaltest5@yandex.ru',
        #     recipient_list=list(users_mails)
        # )


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
        fdata = dict(filter.data.copy())
        for f_name in [str(k) for k in filter.filters]:
            if f_name in fdata:
                for p in fdata[f_name]:
                    filter_params += f"&{f_name}={p}"
        context['filter_params'] = filter_params
        if 'categories' in fdata:
            self.request.session['categories'] = fdata['categories']
            context['filter_by_categories'] = True
        return context


class NewsPostDetail(DetailView):
    model = Post
    context_object_name = "news_post"
    template_name = "news/news_post.html"


class NewsPostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    context_object_name = "news_post"
    template_name = "news/news_delete.html"
    success_url = reverse_lazy('post_list')


class NewsPostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = "news/news_create.html"


class NewsPostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = "news/news_create.html"

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def cat_subscribe(request):
    if 'categories' in request.session:
        categories = request.session['categories']
        if categories is not None:
            user = request.user
            for c_id in categories:
                c = Category.objects.get(id=c_id)
                c.subscribers.add(user)
    return redirect('home')

import datetime

from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import (
    Post,
    UserCategory,
)
from np_6_4.settings import DEFAULT_FROM_EMAIL


def mail_week_posts():
    # week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    week_ago = timezone.now() - datetime.timedelta(days=7)
    users = list(set([uc.user for uc in UserCategory.objects.all()]))
    for u in users:
        if u.email:
            cats = [uc.category for uc in UserCategory.objects.filter(user=u)]  # Список категорий для юзера u
            posts = Post.objects.filter(categories__in=cats, created__gte=week_ago)
            html_content = render_to_string(
                'news/email_posts.html',
                {
                    'posts': posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject='Новости за прошедщую неделю',
                body='',
                from_email=DEFAULT_FROM_EMAIL,
                to=[u.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

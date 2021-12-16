from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import django.core.management.commands.runserver as runserver

from news.dicts import POST_TYPES


POST_PREVIEW_LEN = 124


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through="UserCategory")

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("Author", verbose_name='Автор', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, verbose_name='Категории', through="PostCategory")

    article = "a"
    news = "n"
    type = models.CharField(max_length=1, choices=POST_TYPES, default=article)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= POST_PREVIEW_LEN:
            return self.text
        else:
            return self.text[:POST_PREVIEW_LEN] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})

    def get_full_absolute_url(self):
        cmd = runserver.Command()
        return 'http://' + cmd.default_addr + ':' + cmd.default_port + self.get_absolute_url()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        a_rating = 0  # Рейтинг статей автора
        c_rating = 0  # Рейтинг комментов автора
        ca_rating = 0  # Рейтинг комментов к статьям автора
        for p in Post.objects.filter(author=self, type=Post.article):
            a_rating += p.rating
        a_rating *= 3

        for c in Comment.objects.filter(user=self.user):
            c_rating += c.rating

        for c in Comment.objects.filter(post__author=self):
            ca_rating += c.rating

        self.rating = a_rating + c_rating + ca_rating
        self.save()

    def __str__(self):
        return self.user.username

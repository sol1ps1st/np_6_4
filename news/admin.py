from django.contrib import admin
from news.models import (
    Post,
    Category,
    Comment,
    Author,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)


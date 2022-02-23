from .models import (
    Post,
    Category,
)
from modeltranslation.translator import (
    # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
    register,
    TranslationOptions,
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа@register(Category)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text', )

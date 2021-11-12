from django import template

from utils.bad_word_checker.bad_word_checker import BadWordChecker

checker = BadWordChecker()
register = template.Library()


@register.filter(name='censor')
def censor(value: str):
    if type(value) != str:
        return value
    words = value.split()
    for i, w in enumerate(words):
        if checker.is_bad(w):
            words[i] = "*" * len(w)
    return " ".join(words)

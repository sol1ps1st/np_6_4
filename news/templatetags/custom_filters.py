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


# @register.filter(name='paginate_link')
# def paginate_link(get_dict, page_numer: int):
#     # if type(get_params) != dict:
#     #     raise ValueError("Неверные параметры")
#     href = f"?page={page_numer}"
#     for key, value in get_dict.items():
#         href += f"&{key}={value}"
#     return href

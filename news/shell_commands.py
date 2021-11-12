from django.contrib.auth.models import User

from news.models import (
    Author,
    Comment,
    Post,
    Category,
)


def populate_test_date():
    # 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
    ivanov = User.objects.create_user("Иванов")
    petrov = User.objects.create_user("Петров")

    # 2. Создать два объекта модели Author, связанные с пользователями.
    a_ivanov = Author.objects.create(user=ivanov)
    a_petrov = Author.objects.create(user=petrov)

    # 3. Добавить 4 категории в модель Category.
    cat_sport = Category.objects.create(name="Спорт")
    cat_policy = Category.objects.create(name="Политика")
    cat_cinema = Category.objects.create(name="Кино")
    cat_economy = Category.objects.create(name="Экономика")

    # 4. Добавить 2 статьи и 1 новость.
    article1 = Post.objects.create(
        title="Пандемия и здравоохранение",
        text="Пандемия коронавируса показала неготовность систем здравоохранения и социальной поддержки в мире к"
             " глобальным потрясениям, органам власти необходимо выработать механизмы, чтобы сделать их более устойчивыми"
             " и эффективными, считает глава Счетной палаты РФ",
        author=a_ivanov,
        type=Post.article
    )
    article2 = Post.objects.create(
        title="«Реал» обыграл «Райо Вальекано» и возглавил Примеру",
        text="«Реал» выиграл у «Райо Вальекано» в матче 13-го тура чемпионата Испании. Встреча завершилась со счетом 2:1.",
        author=a_petrov,
        type=Post.article
    )
    news1 = Post.objects.create(
        title="Кудрин оценил потери мировой экономики",
        text="Потери мировой экономики от пандемии коронавируса составляют от $4 трлн до $10 трлн, заявил глава"
             " Счетной палаты Алексей Кудрин.",
        author=a_ivanov,
        type=Post.news
    )

    # 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
    article1.categories.add(cat_policy)
    article2.categories.add(cat_sport)
    news1.categories.add(cat_economy, cat_policy)

    # 6. Создать как минимум 4 комментария к разным объектам модели Post
    # (в каждом объекте должен быть как минимум один комментарий).
    c1 = Comment(
        text="Все плохо, переделывай",
        user=petrov,
        post=article1
    )
    c1.save()
    c2 = Comment(
        text="Ларису Ивановну хочу",
        user=ivanov,
        post=article2
    )
    c2.save()
    c3 = Comment(
        text="Кони все равно лучшие!!!!!!!!",
        user=ivanov,
        post=article2
    )
    c3.save()
    c4 = Comment(
        text="Во всем виноват госдеп!",
        user=petrov,
        post=news1
    )
    c4.save()
    c5 = Comment(
        text="Накатим!",
        user=petrov,
        post=news1
    )
    c5.save()

    # 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
    article1.like()
    article2.dislike()
    news1.like()
    c1.like()
    c2.like()
    c2.dislike()
    c3.dislike()
    c4.like()
    c4.like()
    c4.like()
    c5.like()

    # 8. Обновить рейтинги пользователей.
    a_ivanov.update_rating()
    a_petrov.update_rating()

    # 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
    top_author = Author.objects.order_by("-rating").values("user__username", "rating").first()
    print(top_author["user__username"], top_author["rating"])

    # 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
    # основываясь на лайках/дислайках к этой статье.
    top_article = Post.objects.filter(type=Post.article).order_by("-rating").first()
    print(
        top_article.created.strftime("%m.%d.%Y - %H:%M"),
        top_article.author.user.username,
        top_article.rating,
        top_article.title,
        top_article.preview(),
        sep="\n"
    )

    # 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
    for c in Comment.objects.filter(post=top_article):
        print(
            c.created.strftime("%m.%d.%Y - %H:%M"),
            c.user.username,
            c.rating,
            c.text
        )

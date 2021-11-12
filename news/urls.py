from django.urls import path

from news.views import (
    NewsList,
    NewsPostDetail,
)

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPostDetail.as_view()),
]

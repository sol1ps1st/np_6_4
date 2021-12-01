from django.urls import path

from news.views import (
    NewsList,
    NewsPostDetail,
    NewsPostDelete,
    NewsPostCreate,
    NewsPostUpdate,
)

urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<int:pk>/', NewsPostDetail.as_view(), name='news_detail'),
    path('create/', NewsPostCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', NewsPostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsPostDelete.as_view(), name='news_delete'),
]

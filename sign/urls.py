from django.urls import path

from sign.views import (
    UserProfileUpdate,
    to_authors,
)

urlpatterns = [
    path('user_update/', UserProfileUpdate.as_view(), name='user_update'),
    path('to_authors/', to_authors, name='to_authors'),
]

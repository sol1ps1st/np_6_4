from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
)
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (
    User,
    Group,
)

from news.models import Author


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('post_list')
    template_name = "sign/user_update.html"
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        context["is_author"] = Author.objects.filter(
            user=self.request.user
        ).exists()
        return context


@login_required
def to_authors(request):
    user = request.user
    author, _ = Author.objects.get_or_create(user=user)
    authors_group = Group.objects.get(name='authors')
    if author.user not in authors_group.user_set.all():
        authors_group.user_set.add(user)
    return redirect('home')
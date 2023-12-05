from django.urls import path

from polls import views
from polls.views import (
    PollCreateView,
    PollDeleteView,
    PollDetailView,
    PollListView,
    PollUpdateView,
)

urlpatterns = [
    path("", PollListView.as_view(), name="index"),
    path("poll/<int:pk>", PollDetailView.as_view(), name="poll-view"),
    path("poll/add", PollCreateView.as_view(), name="poll-add"),
    path("poll/edit/<int:pk>", PollUpdateView.as_view(), name="poll-edit"),
    path("poll/delete/<int:pk>", PollDeleteView.as_view(), name="poll-delete"),
    path("option/<int:pk>/vote", views.vote_option, name="option-vote"),
]

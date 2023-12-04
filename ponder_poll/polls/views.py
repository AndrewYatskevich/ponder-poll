import asyncio

import aiohttp
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from polls.forms import (
    PollForm,
    PollOptionCreateFormSet,
    PollOptionUpdateFormSet,
    VoteForm,
)
from polls.models import Option, Poll


class PollCreateView(LoginRequiredMixin, CreateView):
    """
    Create a poll and up to 10 options for it.
    """

    form_class = PollForm
    template_name = "polls/poll-create-edit.html"

    def get_success_url(self):
        return reverse("polls:poll-view", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = PollOptionCreateFormSet(self.request.POST)
        else:
            context["formset"] = PollOptionCreateFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            poll = form.save(commit=False)
            poll.owner = self.request.user
            poll.save()
            self.object = poll
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class PollListView(ListView):
    """
    Return list of polls and some facts from third party API.
    """

    model = Poll
    queryset = Poll.objects.prefetch_related("options", "options__votes").all()
    template_name = "polls/index.html"
    paginate_by = 9

    @staticmethod
    async def _get_fact(session, url):
        async with session.get(url) as response:
            fact = await response.json()
            return fact[0]["fact"]

    async def _get_facts(self, amount):
        actions = []
        async with aiohttp.ClientSession(
            headers={"X-Api-Key": settings.API_NINJAS_KEY}
        ) as session:
            for i in range(amount):
                actions.append(
                    asyncio.ensure_future(
                        self._get_fact(
                            session, "https://api.api-ninjas.com/v1/facts"
                        )
                    )
                )
            facts = await asyncio.gather(*actions)
        return facts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not cache.get("facts", None):
            cache.set("facts", async_to_sync(self._get_facts)(3), 60 * 10)
        context["facts"] = cache.get("facts")
        return context


class PollDetailView(LoginRequiredMixin, DetailView):
    """
    Return the poll by the poll id.
    """

    template_name = "polls/poll-view.html"
    queryset = Poll.objects.prefetch_related("options", "options__votes").all()


class PollUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update the poll and up to 10 of its options.
    """

    model = Poll
    form_class = PollForm
    template_name = "polls/poll-create-edit.html"

    def get_success_url(self):
        return reverse("polls:poll-view", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = PollOptionUpdateFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = PollOptionUpdateFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class PollDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete the poll by the poll id.
    """

    model = Poll
    success_url = reverse_lazy("polls:index")


@login_required
def vote_option(request, pk):
    """
    Create a vote for an option by option id.
    """
    form = VoteForm()
    vote = form.save(commit=False)
    vote.user = request.user
    option = Option.objects.get(pk=pk)
    vote.option = option
    vote.save()
    return redirect(
        reverse_lazy("polls:poll-view", kwargs={"pk": option.poll.id})
    )

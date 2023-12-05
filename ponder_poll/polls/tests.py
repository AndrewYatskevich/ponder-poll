from http import HTTPStatus
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from polls.models import Option, Poll, Vote

User = get_user_model()

POST_POLL_DATA = {
    "options-TOTAL_FORMS": 10,
    "options-INITIAL_FORMS": 0,
    "options-MIN_NUM_FORMS": 0,
    "options-MAX_NUM_FORMS": 1000,
}


class PollTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create(email="test.user@mail.com")
        cls.guest = Client()
        cls.client = Client()

    def setUp(self):
        self.client.force_login(self.owner)
        Poll.objects.bulk_create(
            [
                Poll(text=f"test_poll_{i}", owner=self.owner)
                for i in range(1, 11)
            ]
        )
        poll_10 = Poll.objects.get(text="test_poll_10")
        Option.objects.bulk_create(
            [
                Option(text=f"test_option_{i}", poll=poll_10)
                for i in range(1, 6)
            ]
        )

    def test_get_poll_list(self):
        response = self.guest.get(reverse("polls:index"))
        context = response.context_data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(context.get("facts", False))
        self.assertTrue(context["is_paginated"])

    def test_get_poll_by_pk(self):
        poll = Poll.objects.get(text="test_poll_1")
        response = self.client.get(
            reverse("polls:poll-view", kwargs={"pk": poll.id})
        )
        context = response.context_data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(poll, context["object"])

    def test_create_poll(self):
        data = POST_POLL_DATA.copy()
        data["text"] = "test_poll_new"
        response = self.client.post(
            reverse("polls:poll-add"),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Poll.objects.filter(text="test_poll_new").exists())

    def test_edit_poll(self):
        data = POST_POLL_DATA.copy()
        data["text"] = "test_poll_edited"
        poll = Poll.objects.get(text="test_poll_1")
        response = self.client.post(
            reverse("polls:poll-edit", kwargs={"pk": poll.id}),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Poll.objects.get(text="test_poll_edited"))

    def test_delete_poll_by_pk(self):
        poll = Poll.objects.get(text="test_poll_1")
        response = self.client.delete(
            reverse("polls:poll-delete", kwargs={"pk": poll.id}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_vote(self):
        option = Option.objects.get(text="test_option_1")
        response = self.client.post(
            reverse("polls:option-vote", kwargs={"pk": option.id}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Vote.objects.filter(user=self.owner, option=option).exists()
        )

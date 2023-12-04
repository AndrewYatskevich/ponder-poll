from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count

User = get_user_model()


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.text

    @property
    def total_votes(self):
        votes = Poll.objects.filter(pk=self.pk).aggregate(
            total=Count("options__votes")
        )
        return votes["total"]


class Option(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=200)

    class Meta:
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=("poll", "text"), name="unique_option"
            )
        ]

    def __str__(self):
        return self.text

    @property
    def votes_number(self):
        return self.votes.count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, related_name="votes"
    )

    def validate_unique_vote(self):
        if Vote.objects.filter(
            user=self.user, option__poll=self.option.poll
        ).exists():
            raise ValidationError("Vote must be unique")

    def save(self, *args, **kwargs):
        self.validate_unique_vote()
        super().save(*args, **kwargs)

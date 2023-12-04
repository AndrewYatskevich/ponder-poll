from django.forms import ModelForm, inlineformset_factory
from polls.models import Option, Poll, Vote


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ("text",)


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ("text",)


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = []


PollOptionCreateFormSet = inlineformset_factory(
    Poll, Option, form=OptionForm, extra=10, can_delete=False
)
PollOptionUpdateFormSet = inlineformset_factory(
    Poll, Option, form=OptionForm, extra=10, can_delete_extra=False, max_num=10
)

from django.contrib import admin
from polls.models import Option, Poll, Vote

admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)

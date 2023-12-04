from django.contrib import admin

from polls.models import Option, Poll, Vote


class OptionInline(admin.TabularInline):
    model = Option


class VoteInline(admin.TabularInline):
    model = Vote


class PollAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


class OptionAdmin(admin.ModelAdmin):
    inlines = [VoteInline]


admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Vote)

from csv import DictWriter
from datetime import date, timedelta

from celery import shared_task

from polls.models import Poll


@shared_task
def poll_daily_report():
    yesterday = date.today() - timedelta(days=1)
    polls = Poll.objects.prefetch_related("options", "options__votes").filter(
        created_at__date=yesterday
    )

    with open(
        f"data/reports/{yesterday}_polls_report.csv", "w", newline=""
    ) as file:
        writer = DictWriter(file, fieldnames=["poll", "total_votes"])
        writer.writeheader()
        for poll in polls:
            writer.writerow(dict(poll=poll.text, total_votes=poll.total_votes))

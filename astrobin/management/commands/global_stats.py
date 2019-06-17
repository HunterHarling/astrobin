from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from haystack.query import SearchQuerySet

from astrobin.models import Image, GlobalStat


class Command(BaseCommand):
    help = "Updates the global stats."

    def handle(self, *args, **options):
        sqs = SearchQuerySet()

        users = sqs.models(User).all().count()
        images = sqs.models(Image).all().count()

        integration = 0
        for i in sqs.models(Image).all():
            integration += i.integration
        integration = int(integration / 3600.0)

        gs = GlobalStat(
            users=users,
            images=images,
            integration=integration)
        gs.save()

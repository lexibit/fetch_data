from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'sarabitorvic'
        password = 'sarabitrovic1'

        User.objects.create_superuser(username=username, password=password)

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

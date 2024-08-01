import django
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        try:
            user = User.objects.create(
                email='admin@sky.pro',
                phone='1',
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )

            user.set_password('12345')
            user.save()
        except django.db.utils.IntegrityError:
            pass

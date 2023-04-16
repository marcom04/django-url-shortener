from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--email', help="Superuser's email")
        parser.add_argument('--password', help="Superuser's password")

    def handle(self, *args, **options):
        if not User.objects.filter(email=options['email']).exists():
            User.objects.create_superuser(email=options['email'],
                                          password=options['password'])
            print("Superuser created.")
        else:
            print(f"Superuser '{options['email']}' found on DB: no operations done.")

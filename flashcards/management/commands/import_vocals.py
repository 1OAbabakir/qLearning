import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from flashcards.models import Card

class Command(BaseCommand):
    help = "Importiert Vokabeln aus CSV: es,de"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")
        parser.add_argument("--username", required=True)

    def handle(self, csv_path, username, **kwargs):
        User = get_user_model()
        owner = User.objects.get(username=username)
        with open(csv_path, encoding="utf-8") as f:
            for es, de in csv.reader(f):
                es, de = es.strip(), de.strip()
                if es and de:
                    Card.objects.create(es=es, de=de, owner=owner)
        self.stdout.write(self.style.SUCCESS("Import erfolgreich abgeschlossen."))
        
# command to run:
# python manage.py import_vocals path/to/file.csv --username your_username

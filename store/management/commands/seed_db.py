import os
from pathlib import Path

from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Populate database with fields'

    def handle(self, *args, **options):
        print('Populating database with fields')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        sql = Path(file_path).read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)
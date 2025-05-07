# tasks.py
from celery import shared_task
import pandas as pd
from .models import BibleVersion, BibleVerse
from .views import parse_reference

@shared_task
def process_excel_file(file_path):
    df = pd.read_excel(file_path, header=None)
    version_code = df.iloc[0, 1]
    version_name = df.iloc[1, 1]
    version, created = BibleVersion.objects.get_or_create(code=version_code, defaults={'name': version_name})

    for i in range(2, len(df)):
        reference, text = df.iloc[i, 0], df.iloc[i, 1]
        book, chapter, verse = parse_reference(reference)
        if book and chapter and verse:
            BibleVerse.objects.create(
                version=version,
                book=book,
                chapter=chapter,
                verse=verse,
                text=text
            )

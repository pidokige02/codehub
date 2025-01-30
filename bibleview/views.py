import pandas as pd
import re
from django.shortcuts import render, redirect
from .models import BibleVersion, BibleVerse
from .forms import ExcelUploadForm

def parse_reference(reference):
    """
    'Genesis 1:1' 형태의 문자열을 분리하여 book, chapter, verse를 추출하는 함수.
    """
    match = re.match(r'([\w\s]+)\s(\d+):(\d+)', str(reference))
    if match:
        book = match.group(1).strip()  # 'Genesis'
        chapter = int(match.group(2))  # 1
        verse = int(match.group(3))  # 1
        return book, chapter, verse
    return None, None, None

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            file_path = excel_file.file.path  # 업로드된 파일 경로

            # Excel 데이터 읽기
            df = pd.read_excel(file_path, header=None)  # 헤더 없음 가정

            # 1~2번째 행: 성경 번역본 정보 저장
            version_code = df.iloc[0, 1]  # 예: "ERV"
            version_name = df.iloc[1, 1]  # 예: "English Revised Version"

            # 번역본이 이미 존재하는지 확인 후 저장
            version, created = BibleVersion.objects.get_or_create(
                code=version_code,
                defaults={'name': version_name}
            )

            # 3번째 행부터 성경 구절 저장
            for i in range(2, len(df)):  # 0-based index → 2부터 시작
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

            return redirect('bibleview:bible_list')

    else:
        form = ExcelUploadForm()

    return render(request, 'bibleview/upload_excel.html', {'form': form})

def bible_list(request):
    versions = BibleVersion.objects.all()
    selected_version = request.GET.get('version', None)

    if selected_version:
        verses = BibleVerse.objects.filter(version__code=selected_version).order_by('book', 'chapter', 'verse')
    else:
        verses = BibleVerse.objects.all().order_by('book', 'chapter', 'verse')

    return render(request, 'bibleview/bible_list.html', {'versions': versions, 'verses': verses})

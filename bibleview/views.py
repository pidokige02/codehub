import pandas as pd
import re, math
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import BibleVersion, BibleVerse
from .forms import ExcelUploadForm


combined_to_korean_books = {
    # 한글 약어 → 한글 전체
    "창": "창세기",
    "출": "출애굽기",
    "레": "레위기",
    "민": "민수기",
    "신": "신명기",
    "수": "여호수아",
    "삿": "사사기",
    "룻": "룻기",
    "삼상": "사무엘상",
    "삼하": "사무엘하",
    "왕상": "열왕기상",
    "왕하": "열왕기하",
    "대상": "역대상",
    "대하": "역대하",
    "스": "에스라",
    "느": "느헤미야",
    "에": "에스더",
    "욥": "욥기",
    "시": "시편",
    "잠": "잠언",
    "전": "전도서",
    "아": "아가",
    "사": "이사야",
    "렘": "예레미야",
    "애": "예레미야 애가",
    "겔": "에스겔",
    "단": "다니엘",
    "호": "호세아",
    "욜": "요엘",
    "암": "아모스",
    "옵": "오바댜",
    "욘": "요나",
    "미": "미가",
    "나": "나훔",
    "합": "하박국",
    "습": "스바냐",
    "학": "학개",
    "슥": "스가랴",
    "말": "말라기",
    "마": "마태복음",
    "막": "마가복음",
    "눅": "누가복음",
    "요": "요한복음",
    "행": "사도행전",
    "롬": "로마서",
    "고전": "고린도전서",
    "고후": "고린도후서",
    "갈": "갈라디아서",
    "엡": "에베소서",
    "빌": "빌립보서",
    "골": "골로새서",
    "살전": "데살로니가전서",
    "살후": "데살로니가후서",
    "딤전": "디모데전서",
    "딤후": "디모데후서",
    "딛": "디도서",
    "몬": "빌레몬서",
    "히": "히브리서",
    "약": "야고보서",
    "벧전": "베드로전서",
    "벧후": "베드로후서",
    "요일": "요한일서",
    "요이": "요한이서",
    "요삼": "요한삼서",
    "유": "유다서",
    "계": "요한계시록",

    # 영어 → 한글 전체
    "Genesis": "창세기",
    "Exodus": "출애굽기",
    "Leviticus": "레위기",
    "Numbers": "민수기",
    "Deuteronomy": "신명기",
    "Joshua": "여호수아",
    "Judges": "사사기",
    "Ruth": "룻기",
    "1 Samuel": "사무엘상",
    "2 Samuel": "사무엘하",
    "1 Kings": "열왕기상",
    "2 Kings": "열왕기하",
    "1 Chronicles": "역대상",
    "2 Chronicles": "역대하",
    "Ezra": "에스라",
    "Nehemiah": "느헤미야",
    "Esther": "에스더",
    "Job": "욥기",
    "Psalms": "시편",
    "Psalm": "시편",
    "Proverbs": "잠언",
    "Ecclesiastes": "전도서",
    "Song of Solomon": "아가",
    "Isaiah": "이사야",
    "Jeremiah": "예레미야",
    "Lamentations": "예레미야 애가",
    "Ezekiel": "에스겔",
    "Daniel": "다니엘",
    "Hosea": "호세아",
    "Joel": "요엘",
    "Amos": "아모스",
    "Obadiah": "오바댜",
    "Jonah": "요나",
    "Micah": "미가",
    "Nahum": "나훔",
    "Habakkuk": "하박국",
    "Zephaniah": "스바냐",
    "Haggai": "학개",
    "Zechariah": "스가랴",
    "Malachi": "말라기",
    "Matthew": "마태복음",
    "Mark": "마가복음",
    "Luke": "누가복음",
    "John": "요한복음",
    "Acts": "사도행전",
    "Romans": "로마서",
    "1 Corinthians": "고린도전서",
    "2 Corinthians": "고린도후서",
    "Galatians": "갈라디아서",
    "Ephesians": "에베소서",
    "Philippians": "빌립보서",
    "Colossians": "골로새서",
    "1 Thessalonians": "데살로니가전서",
    "2 Thessalonians": "데살로니가후서",
    "1 Timothy": "디모데전서",
    "2 Timothy": "디모데후서",
    "Titus": "디도서",
    "Philemon": "빌레몬서",
    "Hebrews": "히브리서",
    "James": "야고보서",
    "1 Peter": "베드로전서",
    "2 Peter": "베드로후서",
    "1 John": "요한일서",
    "2 John": "요한이서",
    "3 John": "요한삼서",
    "Jude": "유다서",
    "Revelation": "요한계시록"
}

def parse_reference(reference):
    """
    성경 참조 문자열을 파싱하여 (한글 전체 책 이름, 장, 절)을 반환
    예) '3 John 1:2', '고전13:4', '요일 4:8'
    """

    if pd.isna(reference):
        print ("pd.isna in parse_reference", reference)
        return None, None, None

    reference = reference.strip()

    # 우선 숫자 + 영어 책이름 처리 (e.g., '3 John', '1 Samuel' 등)
    match = re.match(r'(\d\s*\w+(?:\s\w+)*)\s+(\d+):(\d+)', reference)

    if match:
        raw_book = match.group(1).replace("  ", " ").strip()  # '3 John' 등
        chapter = int(match.group(2))
        verse = int(match.group(3))
        full_book = combined_to_korean_books.get(raw_book, f"알 수 없는 책({raw_book})")
        return full_book, chapter, verse

    # 일반 한글/영문 책 이름 (숫자 없는) 처리 (e.g., '창 1:1', 'John 3:16', '요한복음 3:16')
    match = re.match(r'([^\d:]+)\s*(\d+):(\d+)', reference)
    if match:
        raw_book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))
        full_book = combined_to_korean_books.get(raw_book, f"알 수 없는 책({raw_book})")
        return full_book, chapter, verse

    print ("None, None, None in parse_reference")
    return None, None, None

@staff_member_required
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
            print("jinha", version_code, version_name)
            # 번역본이 이미 존재하는지 확인 후 저장
            version, created = BibleVersion.objects.get_or_create(
                code=version_code,
                defaults={'name': version_name}
            )
            print("jinha1", version, created)

            # 3번째 행부터 성경 구절 저장
            first_book, first_chapter = None, None  # 첫 번째 저장된 구절 정보

            for i in range(2, len(df)):  # 0-based index → 2부터 시작
                reference, text = df.iloc[i, 0], df.iloc[i, 1]
                book, chapter, verse = parse_reference(reference)

                if not (book and chapter and verse):
                    print(f"⚠️ 유효하지 않은 구절 건너뜀 → {reference}")
                    continue

                if "알 수 없는 책" in book:
                    print(f"⚠️ 알 수 없는 책 이름 → {reference}")
                    continue

                if book and chapter and verse:
                    BibleVerse.objects.create(
                        version=version,
                        book=book,
                        chapter=chapter,
                        verse=verse,
                        text=text
                    )
                    if first_book is None and first_chapter is None:
                        first_book, first_chapter = book, chapter  # 첫 구절 저장

            # 저장된 첫 번째 책과 장(chapter)으로 리디렉트
            if first_book and first_chapter:
                return redirect(reverse('bibleview:bible_list', args=[first_book, first_chapter]))

    else:
        form = ExcelUploadForm()

    return render(request, 'bibleview/upload_excel.html', {'form': form})



@staff_member_required
def upload_async_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            from .tasks import process_excel_file
            # Celery task 호출
            process_excel_file.delay(excel_file.file.path)
            return JsonResponse({'message': '업로드 완료! 처리 중입니다.'})
    else:
        form = ExcelUploadForm()
    return render(request, 'bibleview/upload_excel.html', {'form': form})




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

@csrf_exempt  # Vue에서 CSRF 토큰이 없을 수 있으므로 예외 처리
# @staff_member_required
def upload_excel_api(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('file')
        if not excel_file:
            return JsonResponse({'error': '파일이 필요합니다.'}, status=400)

        df = pd.read_excel(excel_file, header=None)

        version_code = df.iloc[0, 1]
        version_name = df.iloc[1, 1]

        version, _ = BibleVersion.objects.get_or_create(
            code=version_code,
            defaults={'name': version_name}
        )

        first_book, first_chapter = None, None

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
                if first_book is None:
                    first_book, first_chapter = book, chapter

        if first_book and first_chapter:
            return JsonResponse({
                'book': first_book,
                'chapter': first_chapter,
                'version_code': version.code
            })
        else:
            return JsonResponse({'error': '유효한 구절이 없습니다.'}, status=400)
    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)


from django.shortcuts import render, get_object_or_404
from bibleview.models import BibleVersion, BibleVerse

def bible_list(request, book, chapter):
    # GET 요청에서 선택한 성경 버전 가져오기 (기본값: 첫 번째 버전)
    version_code = request.GET.get("version_code", None)

    # 성경 버전이 유효한지 확인하고, 없으면 기본값 설정
    if version_code:
        version = BibleVersion.objects.filter(code=version_code).first()
    else:
        version = BibleVersion.objects.first()  # 기본값: 첫 번째 성경 버전

    if not version:  # 데이터베이스에 아무 버전도 없을 경우
        return render(request, "bibleview/error.html", {"error": "성경 버전 데이터가 없습니다."})

    version_code = version.code  # 유효한 version_code 사용

    # 해당 책의 모든 장 번호 가져오기
    total_chapters = list(BibleVerse.objects.filter(version=version, book=book)
                          .values_list("chapter", flat=True)
                          .distinct()
                          .order_by("chapter"))

    if not total_chapters:  # 해당 책이 존재하지 않을 경우
        return render(request, "bibleview/error.html", {"error": f"{book}에 대한 데이터가 없습니다."})

    # `chapter`가 정수인지 확인하고, 존재하는 장인지 검증
    try:
        chapter = int(chapter)
        if chapter not in total_chapters:
            return render(request, "bibleview/error.html", {"error": f"{book}에는 {chapter}장이 존재하지 않습니다."})
    except ValueError:  # chapter가 정수가 아닐 경우
        return render(request, "bibleview/error.html", {"error": "잘못된 장 번호입니다."})

    # 선택한 버전, 책, 장에 해당하는 구절 가져오기
    verses = BibleVerse.objects.filter(version=version, book=book, chapter=chapter).order_by("verse")

    # 모든 책 목록 가져오기
    books = list(BibleVerse.objects.filter(version=version).values_list("book", flat=True).distinct())

    # 페이지네이션을 위한 챕터 목록 만들기
    def get_chapter_pagination(chapters, current_chapter):
        max_display = 10  # 한 번에 표시할 최대 개수

        if len(chapters) <= max_display:  # 전체 개수가 적으면 그냥 표시
            return chapters

        result = []
        first, last = chapters[0], chapters[-1]

        # 항상 첫 번째 챕터 추가
        result.append(first)

        if current_chapter > 6:
            result.append("...")  # 앞부분 축약

        # 현재 장을 중심으로 몇 개만 보여주기
        for num in range(current_chapter - 4, current_chapter + 5):
            if first < num < last:
                result.append(num)

        if current_chapter < last - 5:
            result.append("...")  # 뒷부분 축약

        # 항상 마지막 챕터 추가
        result.append(last)
        return result

    paginated_chapters = get_chapter_pagination(total_chapters, chapter)


    return render(request, "bibleview/bible_list.html", {
        "book": book,
        "chapter": chapter,
        "verses": verses,
        "total_chapters": paginated_chapters,  # UI에서 축약된 챕터 리스트 사용
        "version_code": version_code,
        "versions": BibleVersion.objects.all(),  # 템플릿에서 버전 선택 가능하도록 전달
        "books": books,  # 책 목록 추가
    })


from django.http import JsonResponse

def bible_list_api(request, book, chapter):

    # GET 요청에서 선택한 성경 버전 가져오기 (기본값: 첫 번째 버전)
    version_code = request.GET.get("version_code", None)

    # 성경 버전이 유효한지 확인하고, 없으면 기본값 설정
    if version_code:
        version = BibleVersion.objects.filter(code=version_code).first()
    else:
        version = BibleVersion.objects.first()

    if not version:
        return JsonResponse({"error": "성경 버전 데이터가 없습니다."}, status=400)

    version_code = version.code  # 유효한 version_code 사용


    total_chapters = list(BibleVerse.objects.filter(version=version, book=book)
                          .values_list("chapter", flat=True)
                          .distinct()
                          .order_by("chapter"))


    if not total_chapters:
        return JsonResponse({"error": f"{book}에 대한 데이터가 없습니다."}, status=404)

    # `chapter`가 정수인지 확인하고, 존재하는 장인지 검증
    try:
        chapter = int(chapter)
        if chapter not in total_chapters:
            return JsonResponse({"error": f"{book}에는 {chapter}장이 존재하지 않습니다."}, status=400)
    except ValueError:
        return JsonResponse({"error": "잘못된 장 번호입니다."}, status=400)

    # 선택한 버전, 책, 장에 해당하는 구절 가져오기
    # verses = list(BibleVerse.objects.filter(version=version, book=book, chapter=chapter)
    #               .order_by("verse").values("verse", "text"))
    verses = list(BibleVerse.objects.filter(version=version, book=book, chapter=chapter)
                  .order_by("verse").values("verse", "text"))

    # 모든 책 목록 가져오기
    books = list(BibleVerse.objects.filter(version=version)
                 .values_list("book", flat=True).distinct())

    versions = list(BibleVersion.objects.values("code", "name"))


    def get_chapter_pagination(chapters, current_chapter):
        max_display = 10
        if len(chapters) <= max_display:
            return chapters
        result = []
        first, last = chapters[0], chapters[-1]
        result.append(first)
        if current_chapter > 6:
            result.append("...")
        for num in range(current_chapter - 4, current_chapter + 5):
            if first < num < last:
                result.append(num)
        if current_chapter < last - 5:
            result.append("...")
        result.append(last)
        return result

    paginated_chapters = get_chapter_pagination(total_chapters, chapter)


    return JsonResponse({
        "book": book,
        "chapter": chapter,
        "verses": verses,
        "total_chapters": paginated_chapters,
        "version_code": version_code,
        "versions": versions,
        "books": books,
    })

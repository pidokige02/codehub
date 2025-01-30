from django.db import models

from django.db import models

class BibleFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 파일 저장 경로
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간 기록

    def __str__(self):
        return self.file.name

class BibleVersion(models.Model):
    code = models.CharField(max_length=10, unique=True)  # ERV 같은 코드
    name = models.CharField(max_length=100)  # English Revised Version 전체 이름

    def __str__(self):
        return f"{self.code} - {self.name}"

class BibleVerse(models.Model):
    version = models.ForeignKey(BibleVersion, on_delete=models.CASCADE)  # 번역본 연결
    book = models.CharField(max_length=50)  # 책 이름 (예: Genesis)
    chapter = models.IntegerField()  # 장 번호
    verse = models.IntegerField()  # 절 번호
    text = models.TextField()  # 성경 구절

    def __str__(self):
        return f"{self.version.code} {self.book} {self.chapter}:{self.verse} - {self.text[:30]}..."

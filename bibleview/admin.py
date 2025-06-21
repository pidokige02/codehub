from django.contrib import admin

from .models import BibleVerse

@admin.register(BibleVerse)
class BibleVerseAdmin(admin.ModelAdmin):
    list_display = ('version', 'book', 'chapter', 'verse', 'short_text')
    list_filter = ('version', 'book', 'chapter')
    search_fields = ('book', 'text')

    def short_text(self, obj):
        return obj.text[:50] + "..."
    short_text.short_description = 'Text'
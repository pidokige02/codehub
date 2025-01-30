from django import forms
from .models import BibleFile

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = BibleFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        # 파일 확장자 검사 (Excel 파일만 허용)
        if file:
            if not file.name.endswith(('.xls', '.xlsx')):
                raise forms.ValidationError("엑셀 파일 (.xls, .xlsx)만 업로드 가능합니다.")

        return file

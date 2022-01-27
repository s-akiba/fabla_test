from django import forms
from .models import Post,PostReport
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('user_id','user_name', 'email','phone_number','birth','political_faction','icon_photo','bio','assembly')

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = '' # 全フィールドを入力必須


class AppFablaCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'photo', 'category_no', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ReportForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ('report_reason',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ReportForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ('report_reason',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

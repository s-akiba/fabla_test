from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('user_id','user_name', 'email','phone_number','birth','political_faction','icon_photo','bio','assembly')

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = '' # 全フィールドを入力必須

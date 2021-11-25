from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ('user_id','user_name', 'email', 'password1', 'password2')
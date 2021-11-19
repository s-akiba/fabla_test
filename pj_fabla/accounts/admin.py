from django.contrib import admin

# Register your models here.

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.


from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_id','email')


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('user_id', 'user_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    readonly_fields = ('updated_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('user_id', 'user_name', 'email')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('user_id', 'user_name', 'email')
    ordering = ('date_joined',)


admin.site.register(CustomUser, MyUserAdmin)
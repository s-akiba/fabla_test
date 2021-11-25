import datetime
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.base_user import BaseUserManager

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator, RegexValidator
import uuid 

# Create your models here.



class MyUserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, user_id, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not user_id:
            raise ValueError('Users must have an user_id')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)#normalize_emailは正規表現化
        

        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, email, password=None, **extra_fields):#
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, email, password, **extra_fields)#

    def create_superuser(self, user_id, email, password, **extra_fields):#
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id ,email, password, **extra_fields)






class CustomUser(AbstractBaseUser, PermissionsMixin):

    "ユーザーID [PK]"
    user_id = models.CharField(verbose_name='ユーザーID',
                        max_length=20,
                        primary_key=True,
                        help_text='ユーザーIDは一意です。英数字と_(アンダースコア)のみが使用できます。',
                        validators=[MinLengthValidator(3, '3文字以上です！'),RegexValidator(r'^[a-zA-Z0-9_]*$', '英数字と_(アンダースコア)のみです！')],
                        error_messages={
                        'unique': _("A user with that user_id already exists."),
                            },
    )

    user_name = models.CharField(verbose_name='ユーザー名', max_length=30, blank=False)
    email = models.EmailField(verbose_name='メールアドレス', unique=True, blank=False,help_text='入力されたメールアドレスに確認メールが送信されます。')
    phone_number = models.CharField(verbose_name='電話番号', unique=True, blank=False, null=True, default=None, max_length=20)
    birth = models.DateField(verbose_name='生年月日', default=datetime.date.today())
    political_faction = models.CharField(verbose_name='党派', max_length=20)
    icon_photo = models.ImageField(verbose_name='アイコン写真')
    bio = models.TextField(verbose_name='ひとこと',max_length=150)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    is_staff    = models.BooleanField(
                    _('staff status'),
                    default=False,
                    help_text=_('Designates whether the user can log into this admin site.'),
                )

    is_active   = models.BooleanField(
                    _('active'),
                    default=True,
                    help_text=_(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                    ),
                )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects     = MyUserManager()

    EMAIL_FIELD     = 'email'
    USERNAME_FIELD  = 'user_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = 'ユーザー'
        #abstract            = True         #←ここをコメントアウトしないとカスタムユーザーモデルは反映されず、マイグレーションエラーを起こす。

    def clean(self):
        super().clean()
        self.email  = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        return self.user_name

    def get_short_name(self):
        return self.user_name


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# カスタム ユーザーマネージャー
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def get_by_natural_key(self, email):  # 追加
        return self.get(email=email)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    email = models.EmailField(unique=True, null=False)
    nickname = models.CharField(max_length=50, null=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email
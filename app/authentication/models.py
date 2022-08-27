from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username: str, email: str, password: str) -> 'User':
        if username is None:
            raise TypeError("User must have username")
        if email is None:
            raise TypeError("User must have email")
        if password is None:
            raise TypeError("User must have password")

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=200, unique=True, db_index=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def get_article_count(self):
        return self.articles.count()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'auth_user'

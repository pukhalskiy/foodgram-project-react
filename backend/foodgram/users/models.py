from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser

from core.constants import (NAME_MAX_LENGTH, ROLE_MAX_LENGHT,
                            PASSWORD_MAX_LENGHT)


class User(AbstractUser):
    """Кастомная модель пользователя. Регистрация по email."""
    USER = 'user'
    ADMIN = 'admin'
    ROLE_USER = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    ]
    username = models.CharField('Логин', max_length=NAME_MAX_LENGTH,
                                unique=True)
    first_name = models.CharField('Имя', max_length=NAME_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=NAME_MAX_LENGTH)
    email = models.EmailField('email-адрес', unique=True)
    role = models.CharField(max_length=ROLE_MAX_LENGHT, choices=ROLE_USER,
                            default=USER, verbose_name='Пользовательская роль')
    password = models.CharField(max_length=PASSWORD_MAX_LENGHT,
                                verbose_name='Пароль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Подписки на авторов рецептов."""
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='follower', on_delete=models.CASCADE,
                             help_text='Текущий пользователь')
    author = models.ForeignKey(User, verbose_name='Подписка',
                               related_name='followed',
                               on_delete=models.CASCADE,
                               help_text='Подписаться на автора рецепта(ов)')

    class Meta:
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_following')]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'

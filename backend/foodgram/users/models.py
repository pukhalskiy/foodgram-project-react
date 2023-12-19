from django.db import models
from django.db.models import Q, F

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Кастомная модель пользователя. Регистрация по email.'''
    USER = 'user'
    ADMIN = 'admin'
    ROLE_USER = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    ]
    username = models.CharField('Логин', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField('email-адрес', unique=True)
    role = models.CharField(max_length=15, choices=ROLE_USER,
                            default=USER, verbose_name='Пользовательская роль')
    password = models.CharField(max_length=150, verbose_name='Пароль')
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
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Текущий пользователь')
    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
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

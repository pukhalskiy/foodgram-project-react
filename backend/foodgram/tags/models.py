from django.db import models


class Tags(models.Model):
    RED = 'FF0000'
    GREEN = '008000'
    BLUE = '0000FF'
    COLOR_TAG = [
        (RED, 'Красный'),
        (GREEN, 'Зелёный'),
        (BLUE, 'Синий')
    ]
    name = models.CharField(verbose_name='Название тега', unique=True,
                            max_length=150, help_text='Введите название тега')
    color = models.CharField(verbose_name='HEX цвета', unique=True,
                             default=GREEN, choices=COLOR_TAG,
                             help_text='Выберите цвета')
    slug = models.SlugField(verbose_name='Слаг', max_length=150,
                            unique=True, help_text='Укажите слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __srt__(self):
        return f'{self.name}'

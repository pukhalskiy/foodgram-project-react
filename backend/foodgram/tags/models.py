from django.db import models


class Tags(models.Model):
    '''Модель для тегов рецепта.'''
    name = models.CharField(verbose_name='Название тега', unique=True,
                            max_length=150, help_text='Введите название тега')
    color = models.CharField(verbose_name='HEX цвета', unique=True,
                             help_text='Выберите цвета', db_index=False)
    slug = models.SlugField(verbose_name='Слаг', max_length=150,
                            unique=True, help_text='Укажите слаг',
                            db_index=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __srt__(self):
        return f'{self.name}'

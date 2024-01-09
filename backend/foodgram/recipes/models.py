from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator

from core.constants import (MIN_AMOUNT_INREDIENTS, NAME_MAX_LENGTH,
                            COLOR_MAX_LENGHT, SLUG_MAX_LENGHT,
                            CHAR_FIELD_MAX_LENGTH)
from users.models import User


class Tags(models.Model):
    """Модель для тегов рецепта."""
    name = models.CharField(verbose_name='Название тега', unique=True,
                            max_length=NAME_MAX_LENGTH,
                            help_text='Введите название тега')
    color = ColorField(verbose_name='HEX цвета', unique=True,
                       help_text='Выберите цвета', db_index=False,
                       max_length=COLOR_MAX_LENGHT, default='#FF0000')
    slug = models.SlugField(verbose_name='Слаг',
                            max_length=SLUG_MAX_LENGHT,
                            unique=True, help_text='Укажите слаг',
                            db_index=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __srt__(self):
        return f'{self.name}'


class Ingredients(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(verbose_name='Ингридиент',
                            max_length=NAME_MAX_LENGTH,
                            help_text='Введите название ингридиента',
                            db_index=True)

    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=CHAR_FIELD_MAX_LENGTH,
                                        help_text='Укажите единицу измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.name}'


class Recipes(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               help_text='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredients,
                                         verbose_name='Ингридиент',
                                         through='IngredientsForRecipes')
    tags = models.ManyToManyField(Tags, verbose_name='Тег',
                                  help_text='Выберите Тег')
    text = models.TextField(verbose_name='Описание рецепта',
                            help_text='Опишите инструкцию по приготовлению')
    name = models.CharField(verbose_name='Название рецепта',
                            help_text='Введите название рецета',
                            max_length=NAME_MAX_LENGTH,
                            db_index=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления рецепта',)
    image = models.ImageField(verbose_name='Изображение рецепта',
                              help_text='Добавьте изображение рецепта',
                              upload_to='media/')
    pub_date = models.DateTimeField(verbose_name='Время публикации',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'recipes'


class IngredientsForRecipes(models.Model):
    """
    Ингредиенты для рецепта. Промежуточная модель мужду Recipes и Ingredients.
    """
    recipe = models.ForeignKey(Recipes, related_name='recipes_ingredients',
                               verbose_name='Рецепт', on_delete=models.CASCADE,
                               help_text='Выберите рецепт')
    ingredient = models.ForeignKey(Ingredients, related_name='ingredient',
                                   verbose_name='Ингридиент',
                                   on_delete=models.CASCADE,
                                   help_text='Выберите Ингридиет')
    amount = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(
            MIN_AMOUNT_INREDIENTS,
            f'Минимальное количество ингридиентов {MIN_AMOUNT_INREDIENTS}')],
        verbose_name='Количество ингридиента',
        help_text='Укажите количество ингридиента')


class BaseModelForShoppingCartAndRecipes(models.Model):
    """Абстрактная модель для классов Favorites и ShoppingCart."""
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        abstract = True


class Favorites(BaseModelForShoppingCartAndRecipes):
    """Модель для избранных рецептов."""
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorite'

    def __str__(self):
        return f'{self.recipe} в избранном'


class ShoppingCart(BaseModelForShoppingCartAndRecipes):
    """Модель для продуктовой корзины."""
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Список покупок'
        default_related_name = 'shopping_cart'

    def __str__(self):
        return f'{self.recipe} в корзине'

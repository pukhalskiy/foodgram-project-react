from django.db import models
from django.core.validators import MinValueValidator

from recipes.models import Recipes


class Ingredients(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(verbose_name='Ингридиент',
                            max_length=150,
                            help_text='Введите название ингридиента',
                            db_index=True)

    unit_measure = models.CharField(verbose_name='Единица измерения',
                                    max_length=150,
                                    help_text='Укажите единицу измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}'


class IngredientsForRecipes(models.Model):
    """ПромежутОЧКА"""
    recipe = models.ForeignKey(Recipes, related_name='recipe_ingredient',
                               verbose_name='Рецепт', on_delete=models.CASCADE,
                               help_text='Выберите рецепт')
    ingredient = models.ForeignKey(Recipes, related_name='ingredient',
                                   verbose_name='Ингридиент',
                                   on_delete=models.CASCADE,
                                   help_text='Выберите Ингридиет')
    amount = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное количество ингридиента 1')],
        verbose_name='Количество ингридиента',
        help_text='Укажите количество ингридиента')


class ShoppingCart(models.Model):
    pass

from django.db import models
from django.core.validators import MinValueValidator

from tags.models import Tags
from users.models import User


class Ingredients(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(verbose_name='Ингридиент', max_length=150,
                            help_text='Введите название ингридиента',
                            db_index=True)

    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=150, 
                                        help_text='Укажите единицу измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

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
                            max_length=150, db_index=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления рецепта',
        validators=[MinValueValidator(1, 'Минимальное время приготовления')],)
    image = models.ImageField(verbose_name='Изображение рецепта',
                              help_text='Добавьте изображение рецепта',
                              upload_to='media/')
    pub_date = models.DateTimeField(verbose_name='Время публикации',
                                    auto_now_add=True)
    
    class Meta:
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
        MinValueValidator(1, 'Минимальное количество ингридиента 1')],
        verbose_name='Количество ингридиента',
        help_text='Укажите количество ингридиента')


class Favorites(models.Model):
    """Модель для добавления рецептов в избранное."""
    author = models.ForeignKey(User, related_name='favorite',
                               on_delete=models.CASCADE,
                               verbose_name='Автор рецепта')
    recipe = models.ForeignKey(Recipes, related_name='favorite',
                               on_delete=models.CASCADE,
                               verbose_name='Рецепты')

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe}'


class ShoppingCart(models.Model):
    """Модель для продуктовой корзины."""
    author = models.ForeignKey(User, related_name='shopping_cart',
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipes, related_name='shopping_cart',
                               verbose_name='Рецепт для приготовления',
                               on_delete=models.CASCADE,
                               help_text='Выберите рецепт для приготовления')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'{self.recipe}'
    

from django.apps import apps
from django.db import models
from django.core.validators import MinValueValidator

#from ingredients.models import Ingredients, IngredientsForRecipes
#from tags.models import Tags
#from users.models import User


#Ingredients = apps.get_model('ingredients', 'Ingredients')
#IngredientsForRecipes = apps.get_model('ingredients', 'IngredientsForRecipes')


#class Recipes(models.Model):
#    """
#    Модель для рецептов.
#    """
#    author = models.ForeignKey(User, verbose_name='Автор',
#                               on_delete=models.CASCADE,
#                               help_text='Автор рецепта')
#    ingredients = models.ManyToManyField(Ingredients,
#                                         verbose_name='Ингридиент',
#                                         through=IngredientsForRecipes,)
#    tags = models.ManyToManyField(Tags, verbose_name='Тег',
#                                  help_text='Выберите Тег')
#    text = models.TextField(verbose_name='Описание рецепта',
#                            help_text='Опишите инструкцию по приготовлению')
#    name = models.CharField(verbose_name='Название рецепта',
#                            help_text='Введите название рецета',
#                            max_length=150,
#                            db_index=True)
#    cooking_time = models.PositiveSmallIntegerField(
#        verbose_name='Время приготовления',
#        help_text='Укажите время приготовления рецепта',
#        validators=[MinValueValidator(1, 'Минимальное время приготовления')],)
#    image = models.ImageField(verbose_name='Изображение рецепта',
#                              help_text='Добавьте изображение рецепта',
#                              upload_to='media/')
#    pub_date = models.DateTimeField(verbose_name='Время публикации',
#                                    auto_now_add=True)
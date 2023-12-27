from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import format_html

from .models import (IngredientsForRecipes, Recipes, Ingredients, Favorites,
                     ShoppingCart, Tags)


@register(Favorites)
class FavoriteAdmin(ModelAdmin):
    """Адмминистрирование избранных рецептов."""
    list_display = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('author',)


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    """Администрирование покупок."""
    list_display = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('author',)


@register(IngredientsForRecipes)
class IngredientRecipeAdmin(ModelAdmin):
    """Администрирование ингридентов для рецептов."""
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient')
    search_fields = ('name',)


@register(Recipes)
class RecipeAdmin(ModelAdmin):
    """Администрирование рецептов."""
    list_display = ('id', 'author', 'name', 'pub_date', 'in_favorite', )
    search_fields = ('name',)
    list_filter = ('pub_date', 'author', 'name', 'tags')
    filter_horizontal = ('ingredients',)
    empty_value_display = '-пусто-'

    @display()
    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = 'Добавленные рецепты в избранное'


@register(Ingredients)
class IngredientAdmin(ModelAdmin):
    """
    Администрирвоание ингридиентов.
    """
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@register(Tags)
class TagAdmin(ModelAdmin):
    '''Администрирование тэгов'''
    list_display = ("name", "slug", "color_code")
    search_fields = ("name", "color")

    save_on_top = True
    empty_value_display = 'Значение не указано'

    @display(description="Colored")
    def color_code(self, obj: Tags):
        return format_html(
            '<span style="color: #{};">{}</span>', obj.color[1:], obj.color
        )

    color_code.short_description = "Цветовой код тэга"

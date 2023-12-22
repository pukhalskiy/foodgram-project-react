from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status


from tags.models import Tags
from recipes.models import (Recipes, Favorites, ShoppingCart,
                            IngredientsForRecipes, Ingredients)
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор модели User.'''
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredients."""
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tags."""
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class AddIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор поля ingredients, модели Recipes для создание ингредиентов.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор связаной модели Recipes и Ingredients."""
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Recipes для создания, обновления и удаления рецептов.
    """
    ingredients = AddIngredientSerializer(
        many=True,
        write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipes
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Нужно выбрать ингредиент!'})
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, name=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Ингридиенты повторяются!'})
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': 'Количество должно быть больше 0!'})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Нужно выбрать тег!'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Теги повторяются!'})
            tags_list.append(tag)
        return value

    def to_representation(self, instance):
        ingredients = super().to_representation(instance)
        ingredients['ingredients'] = IngredientRecipeSerializer(
            instance.recipes_ingredients.all(), many=True).data
        return ingredients

    def add_tags_ingredients(self, ingredients, tags, model):
        for ingredient in ingredients:
            IngredientsForRecipes.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных из модели Recipes.
    """
    author = UserSerializer()
    tags = TagsSerializer(
        many=True,
        read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredients_ingredients',
        read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorites.objects.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShoppingCart.objects.filter(recipe=obj).exists()
        return False


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели Cart."""
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'coocking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Favorites."""
    name = serializers.ReadOnlyField(
        source='recipes.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipes.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipes.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipes',
        read_only=True)

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'image', 'coocking_time')


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Сериализатор предназначен для вывода рецептом в FollowSerializer."""
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'cooking_time', 'image')


class FollowSerializer(serializers.ModelSerializer):
    """Serializer для модели Follow."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(
                user=obj.user,
                author=obj.author).exists()
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipes.objects.filter(author=obj.author)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipeMiniSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj.author).count()

    def validate(self, data):
        author = self.context.get('author')
        user = self.context.get('request').user
        if Follow.objects.filter(
                author=author,
                user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST)
        if user == author:
            raise ValidationError(
                detail='Невозможно подписаться на себя!',
                code=status.HTTP_400_BAD_REQUEST)
        return data

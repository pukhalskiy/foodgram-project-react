from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action


from .models import Recipes, ShoppingCart, Favorites, Ingredients
from api.serializers import (IngredientSerializer, RecipeWriteSerializer,
                             RecipeListSerializer, ShoppingCartSerializer,
                             FavoriteSerializer)
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsOwnerOrAdminOrReadOnly
from api.paginations import ApiPagination
from users.models import User
from api.services import shopping_cart


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """Вьюсет моедли ингридиентов."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Recipes.
    Позволяет получить, добавить или удалить рецепт из списка покупок и
    избранного пользователя.
    Загрузка списка продуктов.
    """
    queryset = Recipes.objects.all()
    permission_classes = (IsOwnerOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = ApiPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(author=user,
                                           recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = ShoppingCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not ShoppingCart.objects.filter(author=user,
                                           recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        ShoppingCart.objects.get(recipe=recipe).delete()
        return Response('Рецепт удалён из списка покупок',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if Favorites.objects.filter(author=user,
                                        recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not Favorites.objects.filter(author=user,
                                        recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        Favorites.objects.get(recipe=recipe).delete()
        return Response('Рецепт успешно удалён из избранного.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        author = User.objects.get(id=self.request.user.pk)
        if author.shopping_cart.exists():
            return shopping_cart(self, request, author)
        return Response('Список покупок пуст.',
                        status=status.HTTP_404_NOT_FOUND)

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from tags.views import TagsViewSet
from recipes.views import IngredientsViewSet, RecipesViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from .models import Tags
from api.serializers import TagsSerializer


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет для тегов."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny, )

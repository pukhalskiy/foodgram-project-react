from rest_framework.pagination import PageNumberPagination

from core.constants import POSTS_ON_PAGE


class ApiPagination(PageNumberPagination):
    """Паджинация для отображения 6 рецептов на странице."""
    page_size_query_param = "limit"
    page_size = POSTS_ON_PAGE

from rest_framework.pagination import PageNumberPagination


class ApiPagination(PageNumberPagination):
    '''Паджинация для отображения 6 рецептов на странице.'''
    page_size_query_param = "limit"
    page_size = 6

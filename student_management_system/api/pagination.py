from  rest_framework.pagination import(
    LimitOffsetPagination,
    PageNumberPagination
)

class StudentPagination(LimitOffsetPagination):
    
    default_limit = 5
    max_limit = 10

class StudentPagePagination(PageNumberPagination):
    page_size = 2
    
from rest_framework.pagination import LimitOffsetPagination, CursorPagination

class CustomPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit=100
    
class CursorCustomPagination(CursorPagination):
    page_size=2
    ordering=['-created_at']
    cursor_query_param='cursor'
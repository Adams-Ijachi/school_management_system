from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters


class ResultListFilter(filters.BaseFilterBackend):
   def filter_queryset(self, request, queryset, view):
       print(queryset.filter(student_id=request.user))
       return queryset.filter(student_id=request.user)
       
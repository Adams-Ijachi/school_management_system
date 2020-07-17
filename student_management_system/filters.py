
import django_filters
from django.db.models import Q
from django_filters import filters
from django import forms

from .models import *


class StudentFilter(django_filters.FilterSet):
    admin = filters.CharFilter(method='custom_name', label='Name',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Search By Name',
                                                             'style':'width:50%'}))
    grade = filters.ChoiceField(widget=forms.ChoiceField())

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['profile_Image', 'date_created', 'parent', 'gender', 'address']

    def custom_name(self, queryset, names, value):
        names = value.split()
        for val in names:
            q = queryset.filter(Q(admin__first_name__icontains=val) | Q(admin__last_name__icontains=val))
            return q


class StaffFilter(django_filters.FilterSet):
    admin = filters.CharFilter(method='custom_name', label='Name',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Search By Name',
                                                             'style': 'width:50%'}))
    current_position = filters.CharFilter(lookup_expr='icontains', label='Current Position',
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Search By Name',
                                                                        'style': 'width:50%'}))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['profile_Image', 'date_created', 'gender', 'address', 'phone_number']

    def custom_name(self, queryset, names, value):
        names = value.split()
        for val in names:
            q = queryset.filter(Q(admin__first_name__icontains=val) | Q(admin__last_name__icontains=val))
            return q


class ClassFilter(django_filters.FilterSet):
    grade = Class.objects.all()
    grade_list = []
    for grades in grade:
        grade_choice = (grades.id, grades.class_name)
        grade_list.append(grade_choice)

    class_name = filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': ' search class name',
                                                                  'style': 'width:50%'}))
    form_master = filters.CharFilter(lookup_expr='icontains', method='custom_name', label='Name',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Search By Name',
                                                                   'style': 'width:50%'}))

    class Meta:
        model = Class
        fields = '__all__'
        exclude = ['session_year_id', 'date_created', 'updated_at']

    def custom_name(self, queryset, names, value):
        names = value.split()
        for val in names:
            q = queryset.filter(Q(form_master__admin__first_name__icontains=val)
                                | Q(form_master__admin__last_name__icontains=val))
            return q
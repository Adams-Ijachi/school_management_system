from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from ..models import Student, CustomUser, StudentResult



from .serializer import StudentSerializer, StudentCreateSerializer, StudentResultViewSerializer, UserLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins , viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import OwnerOfResult
from .filter import ResultListFilter
from .pagination import StudentPagination, StudentPagePagination
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
# Create your views here.

class StudentViewset( mixins.ListModelMixin,viewsets.GenericViewSet, mixins.UpdateModelMixin,mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    pagination_class = StudentPagePagination
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            self.perform_destroy(instance)
            
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def perform_destroy(self, instance):
        
        user = get_object_or_404(CustomUser, id=instance.admin.id )
        user.delete()




class StudentCreateViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = StudentCreateSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser]
    


class StudentViewResult(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = StudentResultViewSerializer
    queryset = StudentResult.objects.all()
    # permission_classes = [OwnerOfResult]

    def get_queryset(self):
        user_pk = self.request.user
        current_user = get_object_or_404(Student, admin=user_pk)
        new_queryset =  StudentResult.objects.filter(student_id=current_user).exists()
        if new_queryset:
            return StudentResult.objects.filter(student_id=current_user).order_by('-created_at')
        else:
            return Response(detail={"Failure": "error"},status=status.HTTP_204_NO_CONTENT)
        
    # def get_serializer(self, *args, **kwargs):
    #         # checking for post only so that 'get' won't be affected
    #     print('kk')
   
    # # def get_queryset(self, data):
    # #     user = data
    # #     student_ext = get_object_or_404(Student, admin=user)
    # #     print('jj')
    # #     queryset =  StudentResult.objects.filter(student_id=student_ext).exists()
    # #     if queryset:
    # #         return StudentResult.objects.filter(student_id=student_ext)


   
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     result = [ x.values()[0] for x in serializer.data ]
    #     return Response(result)


class UserloginApiview(APIView):
    permission_classes = [AllowAny]
    serializer_class =  UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer =  UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
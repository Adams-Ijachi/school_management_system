
from django.urls import path, include

# from views import  StudentViewset
from rest_framework.routers import DefaultRouter


from .views import StudentViewset ,  StudentCreateViewset , StudentViewResult, UserloginApiview

router = DefaultRouter()
router.register('students', StudentViewset , basename='students')
router.register('create-student', StudentCreateViewset , basename='students_create')
router.register('result-api', StudentViewResult, basename='student_result')
urlpatterns = [
    
    path('viewset/', include(router.urls), name='school-api'),
    path('viewset/<int:index>/', include((router.urls,'api'),namespace='api')),
    path('viewset-create/', include(router.urls)),
    path('view/', include(router.urls)),
    path('viewresult/', include(router.urls)),
    path('login', UserloginApiview.as_view(), name='login')
    # path('article/',  Article_list_VIEW.as_view(), name='articles'),
    # path('article/<int:index>/', Article_detail_VIEW.as_view(), name='article_detail')
]
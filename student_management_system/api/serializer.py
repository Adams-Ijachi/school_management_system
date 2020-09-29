from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, EmailField, CharField
from ..models import Student,CustomUser, Class, Parent, StudentResult

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from django.db.models import Q
from rest_framework.validators import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email']
        read_only_fields = ['email']


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username', 'password', 'email']
        extra_kwargs = {'password':{'write_only':True}
        }



class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentCreateSerializer(serializers.ModelSerializer):
    admin = UserSerializerCreate()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('admin')
        
        user_data_parent  = validated_data.pop('parent').id
        user_data_grade  = validated_data.pop('grade').id
        user_data_student = validated_data
        username = user_data['username']
        first_name = user_data['first_name']
        email = user_data['email']
        last_name = user_data['last_name']
        password = user_data['password']
      
        if 'profile_Image' in user_data_student.keys():
            profile_Image = user_data_student['profile_Image']
        else:
            profile_Image = ''
        if 'address' in user_data_student.keys():
            address = user_data_student['address']
        else:
            address = ''
        if 'gender' in user_data_student.keys():
            gender = user_data_student['gender']
        else:
            gender = ''
       

        
        
        
        user = CustomUser.objects.create_user(username=username, password=password,
                                                             email=email, first_name=first_name,
                                                             last_name=last_name, user_type=3)
        user.save()
        if user:
            student_obj = get_object_or_404(Student, admin=user)
            parent_obj = Parent.objects.get(id=user_data_parent)
            grade_obj = Class.objects.get(id=user_data_grade)
            student_obj.gender = gender
            student_obj.profile_Image = profile_Image
            student_obj.address = address
            student_obj.grade = grade_obj
            student_obj.parent = parent_obj
            student_obj.save()

        
        
        
     
     
        

        return student_obj


      

class StudentSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    url = HyperlinkedIdentityField(
        view_name='d:students-detail',
        
    )
    # grade = ChoicesField
    
    # parents = Parent.objects.all()
    # parent_list = []
    # for person in parents:
    #     person_name = (f'{person.id}' : f'{person.admin.first_name} {person.admin.last_name}')
    #     parent_list.append(person_name)
    # parent = serializers.ChoiceField(label='Parent',
    #                            choices=parent_list,
    #                            )
    
    class Meta:
        model = Student
        fields = ['url', 'admin']
    

    
    
    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('admin')
        # response_dict = validated_data
        student_obj = CustomUser.objects.get(id=instance.admin_id)
        student_obj.first_name = user_data['first_name']
        student_obj.username = user_data['username']
        student_obj.last_name = user_data['last_name']
        '''
        class_id = response_dict['grade'].id #student_class id
        parent_id = response_dict['parent'].id#student_parent id
        parent_obj = get_object_or_404(Parent, pk=parent_id)
        grade_obj = get_object_or_404(Class, pk=class_id)
    
      
        # student_obj.grade = grade_obj
        instance.grade = grade_obj
        instance.parent = parent_obj
         
        instance.address = validated_data.get('address',instance.address )
        instance.gender = validated_data.get('gender',instance.gender )
        instance.profile_Image = validated_data.get('profile_Image', instance.profile_Image )
        
        '''
        student_obj.save()
        instance.save()
        return instance
          



class StudentResultViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResult
        fields = '__all__'

    
    # def get_serializer(self, *args, **kwargs):
    #     print('kk')

    # def __init__(self, data):
    #     user = data
    #     student_ext = get_object_or_404(Student, admin=user)
    #     result_ext = StudentResult.objects.filter(student_id=student_ext).exists()
    #     print(student_ext)
    #     print(result_ext)
    #     if result_ext:
    #         result = StudentResult.objects.filter(student_id=student_ext)
    #         return result
        
        
class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank= True, read_only=True)
    email = EmailField(label='Email')

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {'password':{'write_only':True}
        }

    def validate(self, data):
        email = data.get('email', None)
        password = data['password']
        user = get_object_or_404(CustomUser, email=email)
        if user:
            if user.check_password(password):
                data['token']= 'random number'
                return data
            else:
                raise ValidationError('Incorrect Password')
        else:
            raise ValidationError('email is not valid')

            

      


  
      

        
        
        


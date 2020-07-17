from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
import django.utils.timezone
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, is_active = True, is_staff=False, is_superuser = False, first_name = '',
                    last_name=None,  user_type = 1, username='', password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            user_type = user_type

        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.set_password(password)

        user.save(using=self.db)
        return user

    def create_staffuser(self, email, first_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.create_user(
            email,
            first_name=first_name,
            is_staff=True,
            password=password,
            user_type = 2,

        )

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.create_user(
            email,

            is_staff = True,
            is_superuser=True,
            password = password,

        )

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    first_name = models.CharField(blank=True, max_length=30, null=True)
    last_name = models.CharField(blank=True, max_length=150, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    username = models.CharField(blank=True, max_length=30, null=True)
    date_joined = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    user_type_data = ((1, 'HOD'),
                      (2, 'Staff'),
                      (3, 'Students'),
                      (4, 'Parents'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        return self.is_staff

    @property
    def superuser(self):
        return self.is_superuser

    @property
    def active(self):
        return self.is_active


class Admin(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class Staff(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    profile_Image = models.ImageField(default='default.jpg', upload_to='profile-pic')
    current_position = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.admin.username


class SessionYear(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    term = models.CharField(max_length=20, blank=True)
    objects = UserManager()

    def __str__(self):
        return self.term


class Class(models.Model):
    class_name = models.CharField(max_length=20)
    form_master = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.class_name


class Parent(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    profile_Image = models.ImageField(default='default.jpg', upload_to='profile-pic', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.admin.username


class Student(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    profile_Image = models.ImageField(default='default.jpg', upload_to='profile-pic')
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.admin.username


class Subject(models.Model):
    grade = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject_name = models.CharField(max_length=20)
    subject_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    objects = UserManager()

    def __str__(self):
        return self.subject_name


class Attendance(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.class_id.class_name


class AttendanceReport(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.student_id.admin.username


class FeedbackStudents(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.student_id


class FeedbackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.staff_id


class Notification(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    receiver = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.name


class NotificationReceiver(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    notify = models.ForeignKey(Notification, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.user_id


class StudentResult(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    first_test = models.FloatField(null=True)
    second_test = models.FloatField(null=True)
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.student_id




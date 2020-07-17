from django.contrib import admin

from student_management_system.models import CustomUser, Attendance, AttendanceReport, Notification

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Attendance)
admin.site.register(Notification)


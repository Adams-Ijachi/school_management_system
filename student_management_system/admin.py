from django.contrib import admin

from student_management_system.models import CustomUser, Attendance, AttendanceReport, Notification, StudentResult

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Attendance)
admin.site.register(Notification)
admin.site.register(StudentResult)


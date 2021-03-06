from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from student_management_system import staff_view, student_view, parent_view
from student_management_system.admin_view import StaffList, ClassList, StudentList, SubjectList
from student_management_system.student_view import GeneratePDF
from . import admin_view


urlpatterns = [
    path('', admin_view.home, name='admin_home'),
    path('add_staff/', admin_view.AddStaff, name='add_staff'),
    path('edit_profile', admin_view.edit_profile, name='edit_profile'),
    path('edit_profile_save', admin_view.edit_profile_save, name='edit_profile_save'),
    path('check_email_exist', admin_view.check_email_exist, name='check_email_exist'),
    path('check_username_exist', admin_view.check_username_exist, name='check_username_exist'),
    path('add_staff_save/', admin_view.AddStaffSave, name='add_staff_save'),
    path('add_class/', admin_view.AddClass, name='add_class'),
    path('add_class_save', admin_view.AddClassSave, name='add_class_save'),
    path('add_parent', admin_view.AddParent, name='add_parent'),
    path('add_parent_save', admin_view.AddParentSave, name='add_parent_save'),
    path('add_student', admin_view.AddStudent, name='add_student'),
    path('add_student_save', admin_view.AddStudentSave, name='add_student_save'),
    path('add_subject', admin_view.AddSubject, name='add_subject'),
    path('add_subject_save', admin_view.AddSubjectSave, name='add_subject_save'),
    path('manage_staff', StaffList.as_view(), name='manage_staff'),
    path('manage_class', ClassList.as_view(), name='manage_class'),
    path('manage_parent', admin_view.ParentList, name='manage_parent'),
    path('manage_student', StudentList.as_view(), name='manage_student'),
    path('manage_subject', SubjectList.as_view(), name='manage_subject'),
    path('edit_staff/<int:pk>', admin_view.Staff_update, name='edit_staff'),
    path('edit_staff_save', admin_view.EditStaffSave, name='edit_staff_save'),
    path('edit_class/<int:pk>', admin_view.Class_update, name='edit_class'),
    path('edit_class_save', admin_view.EditClassSave, name='edit_class_save'),
    path('edit_parent/<int:pk>', admin_view.Parent_update, name='edit_parent'),
    path('edit_parent_save', admin_view.EditParentSave, name='edit_parent_save'),
    path('edit_student/<int:pk>', admin_view.Student_update, name='edit_student'),
    path('edit_student_save', admin_view.EditStudentSave, name='edit_student_save'),
    path('edit_subject/<int:pk>', admin_view.Subject_update, name='edit_subject'),
    path('edit_subject_save', admin_view.EditSubjectSave, name='edit_subject_save'),
    path('add_session', admin_view.AddSession, name='add_session'),
    path('add_session_save', admin_view.AddSessionSave, name='add_session_save'),
    path('notification', admin_view.notification, name='notification'),
    path('get_receiver', admin_view.get_receiver, name='get_receiver'),
    path('delete-user/<int:pk>/', admin_view.delete_user, name='user-delete'),
    path('delete-user-parent/<int:pk>/', admin_view.delete_user_parent, name='user-delete-parent'),
    path('delete-user-student/<int:pk>/', admin_view.delete_user_student, name='user-delete-student'),
    path('delete-class/<int:pk>/', admin_view.delete_class, name='delete-class'),
    path('delete-subject/<int:pk>/', admin_view.delete_subject, name='delete-subject'),
    

    path('staff', staff_view.home, name='staff_home'),
    path('take_attendance', staff_view.TakeAttendance, name='take_attendance'),
    path('staff_edit_profile', staff_view.staff_edit_profile, name='staff_edit_profile'),
    path('staff_edit_profile_save', staff_view.staff_edit_profile_save, name='staff_edit_profile_save'),
    path('student_list', staff_view.student_list, name='student_list'),
    path('save_attendance_data', staff_view.save_attendance_data, name='save_attendance_data'),
    path('staff_update_attendance', staff_view.staff_update_attendance, name='staff_update_attendance'),
    path('staff_view_attendance', staff_view.staff_view_attendance, name='staff_view_attendance'),
    path('get_attendance_data', staff_view.get_attendance_data, name='get_attendance_data'),
    path('get_student_attendance', staff_view.get_student_attendance, name='get_student_attendance'),
    path('save_updated_attendance', staff_view.save_updated_attendance, name='save_updated_attendance'),
    path('view_notification', staff_view.view_notification, name='view_notification'),
    path('read_notification/<int:pk>', staff_view.read_notification, name='read_notification'),
    path('staff_add_result', staff_view.staff_add_result, name='staff_add_result'),
    path('add_result_list', staff_view.add_result_list, name='add_result_list'),
    path('staff_edit_result', staff_view.StaffEditResult.as_view(), name='staff_edit_result'),
    path('staff_student_result', staff_view.staff_student_result, name='staff_student_result'),
    path('save_result', staff_view.save_result, name='save_result'),
    path('delete_result', staff_view.delete_result, name='delete_result'),


    path('student_home', student_view.home, name='student_home'),
    path('view_attendance', student_view.view_attendance, name='view_attendance'),
    path('student_view_notification', student_view.view_notification, name='student_view_notification'),
    path('student_session', student_view.student_session, name='student_session'),
   
    path('student_read_notification/<int:pk>', student_view.read_notification, name='student_read_notification'),
    path('student_edit_profile', student_view.student_edit_profile, name='student_edit_profile'),
    path('student_edit_profile_save', student_view.student_edit_profile_save, name='student_edit_profile_save'),
    path('view_result/<int:pk>', student_view.view_result, name='view_result'),
    path('pdf.html/<int:pk>', student_view.GeneratePDF.as_view(), name='pdf'),

    path('parent_home', parent_view.home, name='parent_home'),
    path('child_view_attendance', parent_view.child_view_attendance, name='child_view_attendance'),
    path('get_attendance/<int:pk>', parent_view.get_attendance, name='get_attendance'),
    path('get_result/<int:pk>', parent_view.get_result, name='get_result'),
    path('parent_edit_profile', parent_view.parent_edit_profile, name='parent_edit_profile'),
    path('parent_edit_profile_save', parent_view.parent_edit_profile_save,
         name='parent_edit_profile_save'),
    path('parent_view_notification', parent_view.parent_view_notification, name='parent_view_notification'),
    path('parent_view_result', parent_view.parent_view_result, name='parent_view_result'),
    path('parent_read_notification/<int:pk>', parent_view.parent_read_notification, name='parent_read_notification'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

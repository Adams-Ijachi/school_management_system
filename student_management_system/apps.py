from django.apps import AppConfig


class StudentManagementSystemConfig(AppConfig):
    name = 'student_management_system'

    def ready(self):
        import student_management_system.signals

from django import forms
from django.forms import ChoiceField

from student_management_system.models import Staff, Parent, Class, SessionYear, Subject


class ChoiceValidation(ChoiceField):
    def validate(self, value):
        pass


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(attrs={'class': ''}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': ''}))


class ProfileForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Change Password ?', max_length=50, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'off',
                                                                 'placeholder': 'Enter New Password'}))


class StaffForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    positions = (
        ('teacher', 'TEACHER'),
        ('Nas', 'NAS'),
        ('security', 'SECURITY')
    )
    current_position = forms.ChoiceField(label='Position', choices=positions,
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class StaffProfileForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Change Password ?', max_length=50, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'off',
                                                                 'placeholder': 'Enter New Password'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class StudentProfileForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Change Password ?', max_length=50, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'off',
                                                                 'placeholder': 'Enter New Password'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class ParentProfileForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Change Password ?', max_length=50, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'off',
                                                                 'placeholder': 'Enter New Password'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class AddSessionFrom(forms.Form):
    session_start_year = forms.DateField(label='Session Start',
                                     widget=DateInput(attrs={'class': 'form-control'}),)

    session_end_year = forms.DateField(label='Session End',
                                     widget=DateInput(attrs={'class': 'form-control'}),)
    sections = (
        ('1st', '1st Term'),
        ('2nd', '2nd Term'),
        ('3rd', '3rd Term')
    )

    term = forms.ChoiceField(label='Term', choices=sections, widget=forms.Select(attrs={'class': 'form-control'}))


class ClassForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    teachers = Staff.objects.filter(current_position='teacher')
    teachers_list = []
    for teacher in teachers:
        teacher_name = (teacher.id, f'{teacher.admin.first_name} {teacher.admin.last_name}')
        teachers_list.append(teacher_name)

    form_master = forms.ChoiceField(label='Form_master',
                                    choices=teachers_list,
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    terms = SessionYear.objects.all()
    term_list = []
    for year in terms:
        term = (year.id, f'{year.session_start_year}-TO-{year.session_end_year} {year.term}')
        term_list.append(term)

    session = forms.ChoiceField(label='Session',
                                choices=term_list,
                                widget=forms.Select(attrs={'class': 'form-control'}))


class ParentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    sex = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    gender = forms.ChoiceField(label='Gender', choices=sex, widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class StudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    parents = Parent.objects.all()
    parent_list = []
    for person in parents:
        person_name = (person.id, f'{person.admin.first_name} {person.admin.last_name}')
        parent_list.append(person_name)
    parent = forms.ChoiceField(label='Parent',
                               choices=parent_list,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    grades = Class.objects.all()
    class_list = []
    for i in grades:
        grade_name = (i.id, i.class_name)
        class_list.append(grade_name)
    grade = forms.ChoiceField(label='Class',
                              choices=class_list,
                              widget=forms.Select(attrs={'class': 'form-control'}))

    sex = (
        ('Male', 'Male'),
        ('Female', 'Female')
         )
    gender = forms.ChoiceField(label='Gender', choices=sex, widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class SubjectForm(forms.Form):
    subject_name = forms.CharField(label='Subject Name', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    teachers = Staff.objects.filter(current_position='teacher')
    teachers_list = []
    for teacher in teachers:
        teacher_name = (teacher.id, f'{teacher.admin.first_name} {teacher.admin.last_name}')
        teachers_list.append(teacher_name)

    subject_teacher = forms.ChoiceField(label='Teacher',
                                        choices=teachers_list,
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    grades = Class.objects.all()
    class_list = []
    for i in grades:
        grade_name = (i.id, i.class_name)
        class_list.append(grade_name)

    grade = forms.ChoiceField(label='Class', choices=class_list, widget=forms.Select(attrs={'class': 'form-control'}))


class EditStaffForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    positions = (
        ('teacher', 'TEACHER'),
        ('Nas', 'NAS'),
        ('security', 'SECURITY')
    )
    current_position = forms.ChoiceField(label='Position', choices=positions,
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class EditClassForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    teachers = Staff.objects.filter(current_position='teacher')
    teachers_list = []
    for teacher in teachers:
        teacher_name = (teacher.id, f'{teacher.admin.first_name} {teacher.admin.last_name}')
        teachers_list.append(teacher_name)

    form_master = forms.ChoiceField(label='Form_master',
                                    choices=teachers_list,
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    terms = SessionYear.objects.all()
    term_list = []
    for year in terms:
        term = (year.id, f'{year.session_start_year}-TO-{year.session_end_year} {year.term}')
        term_list.append(term)

    session = forms.ChoiceField(label='Session',
                                choices=term_list,
                                widget=forms.Select(attrs={'class': 'form-control'}))

#

class EditParentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(label='Phone Number', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    sex = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    gender = forms.ChoiceField(label='Gender', choices=sex, widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class EditStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    parents = Parent.objects.all()
    parent_list = []
    for person in parents:
        person_name = (person.id, f'{person.admin.first_name} {person.admin.last_name}')
        parent_list.append(person_name)
    parent = forms.ChoiceField(label='Parent',
                               choices=parent_list,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    grades = Class.objects.all()
    class_list = []
    for i in grades:
        grade_name = (i.id, i.class_name)
        class_list.append(grade_name)
    grade = forms.ChoiceField(label='Class',
                              choices=class_list,
                              widget=forms.Select(attrs={'class': 'form-control'}))

    sex = (
        ('Male', 'Male'),
        ('Female', 'Female')
         )
    gender = forms.ChoiceField(label='Gender', choices=sex, widget=forms.Select(attrs={'class': 'form-control'}))

    profile_Image = forms.ImageField(label='Profile Pic', max_length=50,
                                     required=False)


class EditSubjectForm(forms.Form):
    subject_name = forms.CharField(label='Subject Name', max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    teachers = Staff.objects.filter(current_position='teacher')
    teachers_list = []
    for teacher in teachers:
        teacher_name = (teacher.id, f'{teacher.admin.first_name} {teacher.admin.last_name}')
        teachers_list.append(teacher_name)

    subject_teacher = forms.ChoiceField(label='Teacher',
                                        choices=teachers_list,
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    grades = Class.objects.all()
    class_list = []
    for i in grades:
        grade_name = (i.id, i.class_name)
        class_list.append(grade_name)

    grade = forms.ChoiceField(label='Class', choices=class_list, widget=forms.Select(attrs={'class': 'form-control'}))


# staff form

class TakeAttendanceForm(forms.Form):

    terms = SessionYear.objects.all()
    term_list = []
    for year in terms:
        term = (year.id, f'{year.term}')
        term_list.append(term)

    session = forms.ChoiceField(label='Session',
                                choices=term_list,
                                widget=forms.Select(attrs={'class': 'form-control'}))


class NotificationForm(forms.Form):
    Name = forms.CharField(label='Name', max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))

    user = (
        ('all', 'All Users'),
        ('staff', 'All Staff'),
        ('teacher', 'All Teachers'),
        ('student', 'All Students'),
        ('parent', 'All Parents'),
    )
    receiver = forms.ChoiceField(label='Receiver', choices=user, widget=forms.Select(attrs={'class': 'form-control'}))


class EditResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.staff_id = kwargs.pop('staff_id')
        super(EditResultForm, self).__init__(*args, **kwargs)

        subject_list = []
        session_list = []

        try:
            subjects = Subject.objects.filter(subject_teacher=self.staff_id)

            for subject in subjects:
                subject_single = (subject.id, subject.subject_name)
                subject_list.append(subject_single)
        except:

            subject_list = []

        try:
            session_obj = SessionYear.objects.all()
            for session in session_obj:
                sessions = (session.id, f'{session.term}Term')
                session_list.append(sessions)
        except:
            session_list = []

        self.fields['subject_id'].choices = subject_list
        self.fields['session_id'].choices = session_list

    subject_id = forms.ChoiceField(label='Subject',
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    session_id = forms.ChoiceField(label='Session',
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    student_id = ChoiceValidation(label='Student',
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    first_test = forms.CharField(label='First Test',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    second_test = forms.CharField(label='Second Test',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))








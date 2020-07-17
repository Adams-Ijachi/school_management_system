from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView


from student_management_system.forms import (StaffForm,
                                             ClassForm,
                                             ParentForm,
                                             StudentForm,
                                             SubjectForm,
                                             EditStaffForm,
                                             EditClassForm,
                                             EditParentForm,
                                             EditStudentForm,
                                             EditSubjectForm,
                                             AddSessionFrom,
                                             NotificationForm,
                                             ProfileForm)

from student_management_system.models import (CustomUser,
                                              Class,
                                              Staff,
                                              Parent,
                                              Subject,
                                              Student,
                                              SessionYear,
                                              Notification,
                                              NotificationReceiver,
                                              Attendance,
                                              AttendanceReport)

from .filters import StudentFilter, StaffFilter, ClassFilter


@login_required
def home(request):
    user = request.user
    if user.user_type == '1':
        class_number = Class.objects.all().count()
        staff_number = Staff.objects.all().count()
        teacher_number = Staff.objects.filter(current_position='teacher').count()
        student_number = Student.objects.all().count()
        sessions = SessionYear.objects.all()
        session_list = []
        attendance_per_session = []
        absent_per_session = []
        present_per_session = []
        class_list = []
        subject_list = []
        student_list = []
        class_obj = Class.objects.all()
        for classes in class_obj:
            subject_per_class = Subject.objects.filter(grade=classes.id).count()
            student_per_class = Subject.objects.filter(grade=classes.id).count()
            subject_list.append(subject_per_class)
            class_list.append(classes.class_name)
            student_list.append(student_per_class)

        for session in sessions:
            session_list.append(session.term)
            attendance = Attendance.objects.filter(session_year_id=session.id).count()
            total_present_session = AttendanceReport.objects.filter(attendance_id__session_year_id=session.id,
                                                                    status=True).count()
            total_absent_session = AttendanceReport.objects.filter(attendance_id__session_year_id=session.id,
                                                                   status=False).count()
            absent_per_session.append(total_absent_session)
            present_per_session.append(total_present_session)
            attendance_per_session.append(attendance)
        return render(request, 'admin/home.html', {'class_number': class_number,
                                                   'staff_number': staff_number, 'student_number': student_number,
                                                   'teacher_number': teacher_number, 'class_list': class_list,
                                                   'subject_list': subject_list, 'student_list': student_list,
                                                   'sessions': session_list,
                                                   'attendance_per_session': attendance_per_session,
                                                   'present_per_session': present_per_session,
                                                   'absent_per_session': absent_per_session })
    else:
        return redirect(reverse('login'))


@login_required
def edit_profile(request):
    user = request.user
    if user.user_type == '1':
        user_obj = CustomUser.objects.get(id=user.id)
        form = ProfileForm()
        form.fields['email'].initial = user_obj.email
        form.fields['first_name'].initial = user_obj.first_name
        form.fields['last_name'].initial = user_obj.last_name
        form.fields['username'].initial = user_obj.username

        return render(request, 'admin/edit_profile.html', {'form': form, 'user':user_obj.id})
    else:
        return redirect(reverse('login'))


@login_required
def edit_profile_save(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = ProfileForm(request.POST)
            user_id = request.session.get('user')
            if form.is_valid():

                user = CustomUser.objects.get(id=user_id)
                user_email = user.email
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if email == user_email:
                    email = user_email
                elif qs.exists():
                    messages.error(request, 'Email is Taken')

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                try:
                    user.email = email
                    user.last_name = last_name
                    user.first_name = first_name
                    user.username = username
                    if password != None and password != '':
                        user.set_password(password)
                    user.save()

                    return redirect(reverse('edit_profile'))
                except:
                    messages.error(request, 'Profile Not Edited')
                    return redirect(reverse('edit_profile'))
            else:
                messages.error(request, 'Profile Not Edited')
                return redirect(reverse('edit_profile'))
    else:
        return redirect(reverse('login'))


@login_required
def AddStaff(request):
    user = request.user
    if user.user_type == '1':
        form = StaffForm()
        return render(request, 'admin/add_staff.html', {'form': form})
    else:
        return redirect(reverse('login'))


@login_required
def AddStaffSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')

        else:
            form = StaffForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if qs.exists():
                    messages.error(request,'Email is Taken')
                    return redirect(reverse('add_staff'))
                password = form.cleaned_data['password']
                address = form.cleaned_data["address"]
                phone_number = form.cleaned_data['phone_number']
                current_position = form.cleaned_data['current_position']
                profile_Image = form.cleaned_data['profile_Image']

                try:
                    user = CustomUser.objects.create_user(username=username, password=password,
                                                          email=email, first_name=first_name,
                                                          last_name=last_name, user_type=2)
                    user.staff.address = address
                    user.staff.phone_number = phone_number
                    user.staff.current_position = current_position
                    user.staff.profile_Image = profile_Image
                    user.save()
                    messages.success(request, 'Staff Added Successfully')
                    return redirect(reverse('add_staff'))
                except:
                    messages.error(request, 'Student Not Added')
                    return redirect(reverse('add_student'))
            else:
                messages.error(request, 'Student Not Added')
                return redirect(reverse('add_student'))
    else:
        return redirect(reverse('login'))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
def AddClass(request):
    user = request.user
    if user.user_type == '1':
        form = ClassForm()
        return render(request, 'admin/add_class.html', {'form': form})
    else:
        return redirect(reverse('login'))


@login_required
def AddClassSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = ClassForm(request.POST)
            if form.is_valid():
                try:
                    class_name = form.cleaned_data['class_name']
                    form_master = form.cleaned_data['form_master']
                    session = form.cleaned_data['session']
                    session_obj = SessionYear.objects.get(id=session)
                    teacher_obj = Staff.objects.get(id=form_master)
                    class_obj = Class(class_name=class_name, form_master=teacher_obj,
                                      session_year_id=session_obj)
                    class_obj.save()
                    messages.success(request, 'Class Added Successfully')
                    return redirect(reverse('add_class'))
                except:
                    messages.error(request, 'Class Not Added')
                    return redirect(reverse('add_class'))
            else:
                messages.error(request, 'Class  Not Added')
                return redirect(reverse('add_class'))
    else:
        return redirect(reverse('login'))


@login_required
def AddParent(request):
    user = request.user
    if user.user_type == '1':
        form = ParentForm()
        return render(request, 'admin/add_parent.html', {'form': form})
    else:
        return redirect(reverse('login'))

@login_required
def AddParentSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = ParentForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if qs.exists():
                    messages.error(request, 'Email is Taken')
                    return redirect(reverse('add_parent'))
                password = form.cleaned_data['password']
                address = form.cleaned_data["address"]
                phone_number = form.cleaned_data['phone_number']
                profile_Image = form.cleaned_data['profile_Image']
                gender = form.cleaned_data['gender']
                try:
                    user = CustomUser.objects.create_user(username=username, password=password,
                                                          email=email, first_name=first_name,
                                                          last_name=last_name, user_type=4)
                    user.parent.address = address
                    user.parent.phone_number = phone_number
                    user.parent.profile_Image = profile_Image
                    user.parent.gender = gender
                    user.save()
                    messages.success(request, 'Parent Added Successfully')
                    return redirect(reverse('add_parent'))
                except:
                    messages.error(request, 'Parent Not Added')
                    return redirect(reverse('add_parent'))
            else:
                messages.error(request, 'Parent Not Added')
                return redirect(reverse('add_parent'))
    else:
        return redirect(reverse('login'))


@login_required
def AddStudent(request):
    user = request.user
    if user.user_type == '1':
        form = StudentForm()
        return render(request, 'admin/add_student.html',{'form':form})
    else:
        return redirect(reverse('login'))


@login_required
def AddStudentSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if qs.exists():
                    messages.error(request, 'Email is Taken')
                    return redirect(reverse('add_student'))
                password = form.cleaned_data['password']
                address = form.cleaned_data["address"]

                profile_Image = form.cleaned_data['profile_Image']
                gender = form.cleaned_data['gender']
                parent = form.cleaned_data['parent']
                grade = form.cleaned_data['grade']

                try:
                    user = CustomUser.objects.create_user(username=username, password=password,
                                                          email=email, first_name=first_name,
                                                          last_name=last_name, user_type=3)
                    parent_obj = Parent.objects.get(id=parent)
                    grade_obj = Class.objects.get(id=grade)

                    user.student.gender = gender
                    user.student.address = address

                    user.student.profile_Image = profile_Image
                    user.student.parent = parent_obj
                    user.student.grade = grade_obj
                    user.save()
                    messages.success(request, 'Student Added Successfully')
                    return redirect(reverse('add_student'))
                except:
                    messages.error(request, 'Student Not Added')
                    return redirect(reverse('add_student'))
            else:
                messages.error(request, 'Student Not Added')
                return redirect(reverse('add_student'))
    else:
        return redirect(reverse('login'))


@login_required
def AddSubject(request):
    user = request.user
    if user.user_type == '1':
        form = SubjectForm()
        return render(request, 'admin/add_subject.html', {'form':form})
    else:
        return redirect(reverse('login'))


@login_required
def AddSubjectSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = SubjectForm(request.POST)
            if form.is_valid():
                subject_name = form.cleaned_data['subject_name']
                subject_teacher = form.cleaned_data['subject_teacher']
                grade = form.cleaned_data['grade']

                try:
                    teacher_obj = Staff.objects.get(id=subject_teacher)
                    grade_obj = Class.objects.get(id=grade)
                    subject_obj = Subject(grade=grade_obj, subject_name=subject_name, subject_teacher=teacher_obj)
                    subject_obj.save()
                    messages.success(request, 'Subject Added Successfully')
                    return redirect(reverse('add_subject'))
                except:
                    messages.error(request, 'Subject Not Added')
                    return redirect(reverse('add_subject'))
            else:
                messages.error(request, 'Subject  Not Added')
                return redirect(reverse('add_subject'))
    else:
        return redirect(reverse('login'))


class StaffList(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'admin/manage_staff.html'
    context_object_name = 'staff'
    ordering = ['id']

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.user_type != '1':
            return redirect(reverse('login'))
        else:
            staff = Staff.objects.all()
            myFilter = StaffFilter(request.GET, queryset=staff)
            staff = myFilter.qs
            return render(request, 'admin/manage_staff.html', {'staff': staff, 'myFilter':myFilter})


class ClassList(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'admin/manage_class.html'
    context_object_name = 'grade'
    ordering = ['id']

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_type != '1':
            return redirect(reverse('login'))
        else:
            grade = Class.objects.all()
            myFilter = ClassFilter(request.GET, queryset=grade)
            grade = myFilter.qs
            return render(request, 'admin/manage_class.html', {'grade': grade, 'myFilter': myFilter})


@login_required
def ParentList(request):
    user = request.user
    if user.user_type == '1':
        context = {
            'parents': Parent.objects.all().order_by('id'),
            'students': Student.objects.all()
        }
        return render(request, 'admin/manage_parent.html', context)
    else:
        return redirect(reverse('login'))


@login_required
def AddSession(request):
    user = request.user
    if user.user_type == '1':
        form = AddSessionFrom()
        return render(request, 'admin/add_session.html', {'form': form})


@login_required
def AddSessionSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = AddSessionFrom(request.POST)
            if form.is_valid():
                session_start_year = form.cleaned_data['session_start_year']
                session_end_year = form.cleaned_data['session_end_year']
                term = form.cleaned_data['term']
                try:
                    session_obj = SessionYear(session_start_year=session_start_year,session_end_year =session_end_year
                                              ,term=term)
                    session_obj.save()
                    messages.success(request, 'Session Added Successfully')
                    return redirect(reverse('add_session'))
                except:
                    messages.error(request, 'Session Not Added')
                    return redirect(reverse('add_session'))
            else:
                messages.error(request, 'Session Not Added')
                return redirect(reverse('add_session'))
    else:
        return redirect(reverse('login'))


class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'admin/manage_student.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_type != '1':
            return redirect(reverse('login'))
        else:
            student = Student.objects.all().order_by('id')
            myFilter = StudentFilter(request.GET, queryset=student)

            student = myFilter.qs
            return render(request, 'admin/manage_student.html', {'student': student, 'myFilter': myFilter})


class SubjectList(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'admin/manage_subject.html'
    context_object_name = 'subject'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_type != '1':
            return redirect(reverse('login'))
        else:
            subject = Subject.objects.all().order_by('id')
            return render(request, 'admin/manage_subject.html', {'subject': subject})


@login_required
def Staff_update(request, pk):
    user = request.user
    if user.user_type == '1':

        request.session['staff_id'] = pk
        staff = Staff.objects.get(id=pk)
        request.session['user'] = staff.admin.id
        form = EditStaffForm()
        form.fields['email'].initial = staff.admin.email
        form.fields['first_name'].initial = staff.admin.first_name
        form.fields['last_name'].initial = staff.admin.last_name
        form.fields['username'].initial = staff.admin.username
        form.fields['address'].initial = staff.address
        form.fields['phone_number'].initial = staff.phone_number
        form.fields['profile_Image'].initial = staff.profile_Image
        form.fields['current_position'].initial = staff.current_position
        return render(request, 'admin/edit_staff.html', {'form': form, 'staff': staff, 'staff_id': pk,
                                                         'user': staff.admin.id})
    else:
        return redirect(reverse('login'))


@login_required
def EditStaffSave(request):
    user = request.user
    if user.user_type == '1':
        pk = request.session.get('staff_id')
        image_obj = Staff.objects.get(id=pk)
        staff_email = image_obj.admin.email
        image = image_obj.profile_Image

        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')

        else:
            staff_id = request.session.get('staff_id')
            user_id = request.session.get('user')
            form = EditStaffForm(request.POST, request.FILES)
            if form.is_valid():
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if email == staff_email:
                    email = staff_email
                elif qs.exists():
                    messages.error(request, 'Email is Taken')
                    return redirect(reverse('edit_staff', kwargs={'pk': staff_id}))
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                address = form.cleaned_data['address']
                phone_number = form.cleaned_data['phone_number']
                current_position = form.cleaned_data['current_position']
                profile_Image = form.cleaned_data['profile_Image']
                if not profile_Image:
                    profile_Image = image
                try:
                    user = CustomUser.objects.get(id=user_id)
                    staff_obj = Staff.objects.get(id=staff_id)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    staff_obj.address = address
                    staff_obj.phone_number = phone_number
                    staff_obj.current_position = current_position
                    staff_obj.profile_Image = profile_Image
                    user.save()
                    staff_obj.save()
                    messages.success(request, 'Staff Edited Successfully')
                    return redirect(reverse('edit_staff', kwargs={'pk': staff_id}))
                except:
                    messages.error(request, 'Staff Not Added')
                    return redirect(reverse('edit_staff', kwargs={'pk': staff_id}))
            else:
                messages.error(request, 'Staff Not Added')
                return redirect(reverse('edit_staff', kwargs={'pk': staff_id}))
    else:
        return redirect(reverse('login'))


@login_required
def Class_update(request, pk):
    user = request.user
    if user.user_type == '1':
        form = EditClassForm()
        grade = Class.objects.get(id=pk)
        request.session['class_id'] = pk

        form.fields['class_name'].initial = grade.class_name
        form.fields['form_master'].initial = grade.form_master.id
        form.fields['session'].initial = grade.session_year_id.id
        return render(request, 'admin/edit_class.html', {'form': form, 'class_id': pk})
    else:
        return redirect(reverse('login'))


@login_required
def EditClassSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            class_id = request.session.get('class_id')
            form = EditClassForm(request.POST)
            if form.is_valid():
                class_name = form.cleaned_data['class_name']
                form_master = form.cleaned_data['form_master']
                session_year_id = form.cleaned_data['session']

                try:
                    teacher_obj = Staff.objects.get(id=form_master)
                    class_obj = Class.objects.get(id=class_id)
                    session_id = SessionYear.objects.get(id=session_year_id)
                    class_obj.session_year_id = session_id
                    class_obj.class_name = class_name
                    class_obj.form_master = teacher_obj
                    class_obj.save()
                    messages.success(request, 'Class Edited Successfully')
                    return redirect(reverse('edit_class', kwargs={'pk': class_id}))
                except:
                    messages.error(request, 'Class Not Added')
                    return redirect(reverse('edit_class', kwargs={'pk':class_id}))
            else:
                messages.error(request, 'Class Not Added')
                return redirect(reverse('edit_class', kwargs={'pk': class_id}))
    else:
        return redirect(reverse('login'))


@login_required
def Parent_update(request, pk):
    user = request.user
    if user.user_type == '1':
        form = EditParentForm()
        parent = Parent.objects.get(id=pk)
        request.session['parent_id'] = pk
        form.fields['email'].initial = parent.admin.email
        form.fields['first_name'].initial = parent.admin.first_name
        form.fields['last_name'].initial = parent.admin.last_name
        form.fields['username'].initial = parent.admin.username
        form.fields['address'].initial = parent.address
        form.fields['gender'].initial = parent.gender
        form.fields['profile_Image'].initial = parent.profile_Image
        form.fields['phone_number'].initial = parent.phone_number
        return render(request, 'admin/edit_parent.html', {'form': form, 'parent_id': parent})
    else:
        return redirect(reverse('login'))


@login_required
def EditParentSave(request):
    user = request.user
    if user.user_type == '1':

        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = EditParentForm(request.POST, request.FILES)
            parent_id = request.session.get('parent_id')
            if form.is_valid():

                parent_obj = Parent.objects.get(id=parent_id)
                parent_email = parent_obj.admin.email
                parent_image = parent_obj.profile_Image
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if email == parent_email:
                    email = parent_email
                elif qs.exists():
                    messages.error(request, 'Email is Taken')
                    return redirect(reverse('edit_parent', kwargs={'pk': parent_id}))

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                address = form.cleaned_data['address']
                phone_number = form.cleaned_data['phone_number']
                profile_Image = form.cleaned_data['profile_Image']
                if not profile_Image:
                    profile_Image = parent_image
                try:
                    user_obj = parent_obj.admin.id
                    user = CustomUser.objects.get(id=user_obj)
                    user.email = email
                    user.last_name = last_name
                    user.first_name = first_name
                    user.username = username
                    parent_obj.address = address
                    parent_obj.profile_Image = profile_Image
                    parent_obj.phone_number = phone_number
                    del request.session['parent_id']
                    user.save()
                    parent_obj.save()
                    messages.success(request, 'Parent Edited Successfully')
                    return redirect(reverse('edit_parent', kwargs={'pk': parent_id}))
                except:
                    messages.error(request, 'Parent Not Added')
                    return redirect(reverse('edit_parent', kwargs={'pk': parent_id}))
            else:
                messages.error(request, 'Parent Not Added')
                return redirect(reverse('edit_parent', kwargs={'pk': parent_id}))
    else:
        return redirect(reverse('login'))


@login_required
def Student_update(request, pk):
    user = request.user
    if user.user_type == '1':

        form = EditStudentForm()
        student_id = Student.objects.get(id=pk)
        request.session['student_id'] = pk
        form.fields['email'].initial = student_id.admin.email
        form.fields['first_name'].initial = student_id.admin.first_name
        form.fields['last_name'].initial = student_id.admin.last_name
        form.fields['username'].initial = student_id.admin.username
        form.fields['address'].initial = student_id.address
        form.fields['gender'].initial = student_id.gender
        form.fields['profile_Image'].initial = student_id.profile_Image
        form.fields['grade'].initial = student_id.grade.id
        form.fields['parent'].initial = student_id.parent.id
        return render(request, 'admin/edit_student.html', {'form': form, 'student_id': student_id})
    else:
        return redirect(reverse('login'))


@login_required
def EditStudentSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = EditStudentForm(request.POST, request.FILES)
            student_id = request.session.get('student_id')
            if form.is_valid():

                student_obj = Student.objects.get(id=student_id)
                student_image = student_obj.profile_Image
                student_email = student_obj.admin.email

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                qs = CustomUser.objects.filter(email=email)
                if email == student_email:
                    email = student_email
                elif qs.exists():
                    messages.error(request, 'Email is Taken')
                    return redirect(reverse('edit_student', kwargs={'pk': student_id}))

                address = form.cleaned_data["address"]
                gender = form.cleaned_data['gender']
                parent = form.cleaned_data['parent']
                grade = form.cleaned_data['grade']
                profile_Image = form.cleaned_data['profile_Image']
                if not profile_Image:
                    profile_Image = student_image

                try:
                    user_obj = student_obj.admin.id
                    user = CustomUser.objects.get(id=user_obj)
                    class_obj = Class.objects.get(id=grade)
                    parent_obj = Parent.objects.get(id=parent)
                    user.email = email
                    user.last_name = last_name
                    user.first_name = first_name
                    user.username = username

                    student_obj.address = address
                    student_obj.profile_Image = profile_Image
                    student_obj.gender = gender
                    student_obj.parent = parent_obj
                    student_obj.grade = class_obj

                    del request.session['student_id']
                    user.save()
                    student_obj.save()
                    messages.success(request, 'Student Edited Successfully')
                    return redirect(reverse('edit_student', kwargs={'pk': student_id}))
                except:
                    messages.error(request, 'Student Not Added')
                    return redirect(reverse('edit_student', kwargs={'pk': student_id}))
            else:
                messages.error(request, 'Student Not Added')
                return redirect(reverse('edit_student', kwargs={'pk': student_id}))
    else:
        return redirect(reverse('login'))


@login_required
def Subject_update(request, pk):
    user = request.user
    if user.user_type == '1':
        form = EditSubjectForm()
        subject_id = Subject.objects.get(id=pk)
        request.session['subject_id'] = pk
        form.fields['subject_name'].initial = subject_id.subject_name
        form.fields['subject_teacher'].initial = subject_id.subject_teacher.id
        form.fields['grade'].initial = subject_id.grade.id
        return render(request, 'admin/edit_subject.html', {'form': form, 'subject_id': subject_id})
    else:
        return redirect(reverse('login'))


@login_required
def EditSubjectSave(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = EditSubjectForm(request.POST)
            subject_id = request.session.get('subject_id')
            if form.is_valid():
                subject_name = form.cleaned_data['subject_name']
                subject_teacher = form.cleaned_data['subject_teacher']
                grade = form.cleaned_data['grade']
                try:
                    teacher_obj = Staff.objects.get(id=subject_teacher)
                    grade_obj = Class.objects.get(id=grade)
                    subject_obj = Subject.objects.get(id=subject_id)
                    subject_obj.subject_name = subject_name
                    subject_obj.subject_teacher = teacher_obj
                    subject_obj.grade = grade_obj
                    subject_obj.save()
                    del request.session['subject_id']

                    messages.success(request, 'Subject Edited Successfully')
                    return redirect(reverse('edit_subject', kwargs={'pk': subject_id}))
                except:
                    messages.error(request, 'Subject Not Added')
                    return redirect(reverse('edit_subject', kwargs={'pk': subject_id}))
            else:
                messages.error(request, 'Subject Not Added')
                return redirect(reverse('edit_subject', kwargs={'pk': subject_id}))
    else:
        return redirect(reverse('login'))


@login_required
def notification(request):
    user = request.user
    if user.user_type == '1':
        form = NotificationForm()
        return render(request, 'admin/message.html', {'form': form})
    else:
        return redirect(reverse('login'))


@csrf_exempt
@login_required
def get_receiver(request):
    user = request.user
    if user.user_type == '1':
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            name = request.POST.get('name')
            description = request.POST.get('description')
            receiver = request.POST.get('receiver')

            list_data = []
            if receiver == 'all':
                user = CustomUser.objects.all()
            elif receiver == 'staff':
                user = CustomUser.objects.filter(user_type=2)
            elif receiver == 'teacher':
                user = Staff.objects.filter(current_position='teacher')
                for people in user:
                    list_data.append(people.admin)
            elif receiver == 'student':
                user = CustomUser.objects.filter(user_type=3)
            else:
                user = CustomUser.objects.filter(user_type=4)
            try:
                notification_obj = Notification(name=name, description=description, receiver=receiver)
                notification_obj.save()

                if not list_data:
                    for i in user:
                        list_data.append(i)

                for val in list_data:
                    custm = CustomUser.objects.get(id=val.id)
                    notify_obj = NotificationReceiver(user_id=custm, notify=notification_obj)
                    notify_obj.save()
                messages.success(request, 'Message Sent Successfully')
                return redirect(reverse('notification'))
            except:
                messages.error(request, 'Message Not Sent')
                return redirect(reverse('notification'))

    else:
        return redirect(reverse('login'))

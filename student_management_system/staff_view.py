import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from student_management_system.forms import StaffProfileForm, EditResultForm
from student_management_system.models import Class, SessionYear, Student, Attendance, AttendanceReport, Notification, \
    NotificationReceiver, CustomUser, Staff, Subject, StudentResult


@login_required
def home(request):
    user = request.user

    if user.user_type != '2':
        return redirect(reverse('login'))

    classes = Class.objects.all()
    class_number = Class.objects.filter(form_master=user.staff.id).count()
    class_num = Class.objects.filter(form_master=user.staff.id)
    subject_num = Subject.objects.filter(subject_teacher=user.staff.id).count()
    class_list = []
    attendance_list = []
    present_list = []
    absent_list = []
    student_id = []
    student_val = []
    for i in class_num:

        student_id.append(i.id)
        total_attendance = AttendanceReport.objects.filter(attendance_id__class_id=i.id).count()
        total_absent = AttendanceReport.objects.filter(attendance_id__class_id=i.id, status=False).count()
        total_present = AttendanceReport.objects.filter(attendance_id__class_id=i.id, status=True).count()

        class_list.append(i.class_name)
        attendance_list.append(total_attendance)
        absent_list.append(total_absent)
        present_list.append(total_present)

    attendance_num = Attendance.objects.filter(class_id__in=student_id).count()
    student_number = Student.objects.filter(grade__in=student_id).count()
    student_data = Student.objects.filter(grade__in=student_id)
    for student in student_data:
        student_val.append(student.id)
    report_absent = AttendanceReport.objects.filter(student_id__in=student_val, status=False).count()
    report_present = AttendanceReport.objects.filter(student_id__in=student_val, status=True).count()

    return render(request, 'staff/home.html', {'class': classes,
                                               'class_number': class_number, 'student_number': student_number,
                                               'subject_num': subject_num, 'attendance_num': attendance_num,
                                               'report_absent': report_absent, 'report_present': report_present,
                                               'class_n': class_list, 'attendance_list': attendance_list,
                                               'absent_list': absent_list, 'present_list': present_list })


@login_required
def TakeAttendance(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))

    form_master = user.staff.id
    class_obj = Class.objects.filter(form_master=form_master)
    class_ext = Class.objects.filter(form_master=form_master).exists()
    if class_ext:
        session_obj = SessionYear.objects.all()
        return render(request, 'staff/take_attendance.html', {'class': class_obj, 'session': session_obj})
    else:
        return HttpResponse('Not A Form Master Of Any Class')


@login_required
def staff_edit_profile(request):
    user = request.user
    if user.user_type != '2':
        return redirect(reverse('login'))
    else:

        form = StaffProfileForm()
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['username'].initial = user.username
        form.fields['address'].initial = user.staff.address
        form.fields['phone_number'].initial = user.staff.phone_number
        form.fields['profile_Image'].initial = user.staff.profile_Image
        return render(request, 'staff/edit_profile.html', {'form': form})


@login_required
def staff_edit_profile_save(request):
    user = request.user
    if user.user_type != '2':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = StaffProfileForm(request.POST, request.FILES)
            image =  user.staff.profile_Image
            if form.is_valid():
                user = CustomUser.objects.get(id=user.id)
                staff = Staff.objects.get(id=user.staff.id)

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                address = form.cleaned_data["address"]
                phone_number = form.cleaned_data['phone_number']
                profile_Image = form.cleaned_data['profile_Image']
                if not profile_Image:
                    profile_Image = image

                try:
                    user.last_name = last_name
                    user.first_name = first_name
                    user.username = username
                    if password is not None and password != '':
                        user.set_password(password)
                    user.save()

                    staff.address = address
                    staff.phone_number = phone_number
                    staff.profile_Image = profile_Image
                    staff.save()
                    if password:
                        return redirect(reverse('staff_edit_profile'))
                    else:
                        messages.success(request, 'Staff Added Successfully')
                        return redirect(reverse('staff_edit_profile'))
                except:
                    messages.error(request, 'Profile Not Edited')
                    return redirect(reverse('staff_edit_profile'))
            else:
                messages.error(request, 'Profile Not Edited')
                return redirect(reverse('staff_edit_profile'))


@login_required
@csrf_exempt
def student_list(request):
    user = request.user
    staff_id = user.staff.id
    class_obj = Class.objects.filter(form_master=staff_id)
    if user.user_type != '2' or user.staff.current_position != 'teacher':

        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:

            class_id = request.POST.get('class')
            student_obj = Student.objects.filter(grade=class_id)
            list_data = []
            for student in student_obj:
                data = (student.id, f'{student.admin.first_name} {student.admin.last_name}')
                list_data.append(data)

            return JsonResponse(list_data, content_type='application/json', safe=False)


@login_required
@csrf_exempt
def save_attendance_data(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            class_id = request.POST.get('class_id')
            session_id = request.POST.get('session_year_id')
            student_id = request.POST.get('student_id')
            attendance_date = request.POST.get('attendance_date')
            data = json.loads(student_id)
            session_obj = SessionYear.objects.get(id=session_id)
            try:
                class_obj = Class.objects.get(id=class_id)
                attendance_obj = Attendance(attendance_date=attendance_date, class_id=class_obj,
                                            session_year_id=session_obj)
                attendance_obj.save()
                for stud in data:
                    student = Student.objects.get(id=stud['id'])
                    attendance_report = AttendanceReport(attendance_id=attendance_obj, student_id=student,
                                                         status=stud['status'],
                                                         )
                    attendance_report.save()
                return HttpResponse('ok')
            except:
                return HttpResponse('fail')


@login_required
def staff_view_attendance(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))

    else:
        return render(request, 'staff/view_student.html')


@login_required
def staff_update_attendance(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        form_master = user.staff.id
        class_obj = Class.objects.filter(form_master=form_master)
        class_ext = Class.objects.filter(form_master=form_master).exists()
        if class_ext:
            session_obj = SessionYear.objects.all()
            attendance_obj = Attendance.objects.all()

            return render(request, 'staff/update_attendance.html',
                          {'class': class_obj, 'attendance_obj': attendance_obj,
                           'session': session_obj})

        else:
            return HttpResponse('Not A Form Master Of Any Class')


@login_required
@csrf_exempt
def get_attendance_data(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        class_id = request.POST.get('class_id')
        session_year_id = request.POST.get('session_year_id')
        class_obj = Class.objects.get(id=class_id)
        session_year_obj = SessionYear.objects.get(id=session_year_id)
        attendance = Attendance.objects.filter(class_id=class_obj,session_year_id=session_year_obj)
        attendance_obj = []
        for single_attendance in attendance:
            data = {'id': single_attendance.id, 'attendance_date': str(single_attendance.attendance_date),
                    'session_year_id': single_attendance.session_year_id.id}
            attendance_obj.append(data)
        return JsonResponse(json.dumps(attendance_obj), safe=False)


@login_required
@csrf_exempt
def get_student_attendance(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:

            attendance_date = request.POST.get('attendance_id')
            attendance_obj = Attendance.objects.get(id=attendance_date)
            attendance_data = AttendanceReport.objects.filter(attendance_id=attendance_obj)

            list_data = []
            for student in attendance_data:
                data = {'id': student.student_id.id, 'Name': f'{student.student_id.admin.first_name}'
                                                             f' {student.student_id.admin.last_name}',
                        'status': student.status}
                list_data.append(data)

            return JsonResponse(list_data, content_type='application/json', safe=False)


@login_required
@csrf_exempt
def save_updated_attendance(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            student_id = request.POST.get('student_id')
            attendance_date = request.POST.get('attendance_date')
            attendance_obj = Attendance.objects.get(id=attendance_date)
            data = json.loads(student_id)
            try:
                for stud in data:
                    student = Student.objects.get(id=stud['id'])
                    attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance_obj)
                    attendance_report.status = stud['status']
                    attendance_report.save()
                return HttpResponse('ok')
            except:
                return HttpResponse('fail')


@login_required
def view_notification(request):
    user = request.user
    if user.user_type != '2' :
        return redirect(reverse('login'))
    else:
        user = request.user.id
        notification_obj = NotificationReceiver.objects.filter(user_id=user).order_by('-created_at')
        return render(request, 'staff/view_attendance.html', {'notice': notification_obj})


@login_required
def read_notification(request, pk):
    user = request.user
    if user.user_type != '2':
        return redirect(reverse('login'))
    else:
        request.session['message_id'] = pk
        message = NotificationReceiver.objects.get(id=pk)
        return render(request, 'staff/read_notification.html', {'message_id': message})


@login_required
def staff_add_result(request):
    user = request.user
    if user.user_type != '2':
        return redirect(reverse('login'))
    else:

        subject_id = Subject.objects.filter(subject_teacher=user.staff.id)

        session_obj = SessionYear.objects.all()
        form_master = user.staff.id
        class_ext = Class.objects.filter(form_master=form_master).exists()
        if class_ext:
            
            return render(request,  'staff/add_result.html', {'subject': subject_id, 'session': session_obj})
        else:
            return HttpResponse('Not A Form Master Of Any Class Cant Add or Edit')


@login_required
@csrf_exempt
def add_result_list(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            subject_id = request.POST.get('subject')
            if subject_id == '':
                return JsonResponse('Please Add Class', content_type='application/json', safe=False,)
            else:
                session_id = request.POST.get('session')
                student_obj = Student.objects.filter(grade__subject__id=subject_id,grade__session_year_id__id=session_id)

                

                list_data = []
                for student in student_obj:
                    data = (student.id, f'{student.admin.first_name} {student.admin.last_name}')
                    list_data.append(data)

                return JsonResponse(list_data, content_type='application/json', safe=False)


@login_required
def save_result(request):
    user = request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            student_id = request.POST.get('student_id')
            subject_id = request.POST.get('subject')
            first_test = request.POST.get('first_test')
            second_test = request.POST.get('second_test')
            session = request.POST.get('session')
            result_ext = StudentResult.objects.filter(session_year_id=session,student_id=student_id, subject_id=subject_id).exists()
              
            if result_ext:
                return JsonResponse('Sorry This Student Result Already Exists For This Session', safe=False)
            else:
                if first_test == '':
                    first_test = 0
                if second_test =='':
                    second_test = 0
                    
                try:
                    student_obj = Student.objects.get(id=student_id)
                    subject_obj = Subject.objects.get(id=subject_id)
                    session_obj = SessionYear.objects.get(id=session)
                
                    result = StudentResult(student_id=student_obj, subject_id=subject_obj,
                                            first_test=first_test, second_test=second_test, session_year_id=session_obj)
                    result.save()
                    messages.success(request, 'Result Added Successfully')
                    return JsonResponse('Result Added Successfully', safe=False)
                except:
                    messages.error(request, 'Result Not Added')
                    return JsonResponse('Result Not Added', safe=False)
            


class StaffEditResult(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user == 'AnonymousUser' or user.user_type != '2' or user.staff.current_position != 'teacher':
            print('k')
        else:
            staff_id = request.user.staff.id
            form = EditResultForm(staff_id=staff_id)
            class_ext = Class.objects.filter(form_master=staff_id).exists()
            if class_ext:
                return render(request, 'staff/edit_result.html', {'form': form})
            else:
                return HttpResponse('Not A Form Master Cant Add or Edit Result')

    def post(self, request,  *args, **kwargs):
        staff_id = request.user.staff.id
       

        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')
        first_test = request.POST.get('first_test')
        second_test = request.POST.get('second_test')
        session = request.POST.get('session_id')
       

        try:
            student_obj = Student.objects.get(id=student_id)
            subject_obj = Subject.objects.get(id=subject_id)
            session_obj = SessionYear.objects.get(id=session)

            if first_test == '':
                first_test = 0
            if second_test == '':
                second_test = 0

            result = StudentResult.objects.get(student_id=student_obj, subject_id=subject_obj,
                                                session_year_id=session_obj)
            result.first_test = first_test
            result.second_test = second_test
            result.save()
            messages.success(request, 'Edited  Successfully')
            return JsonResponse('True',safe=False)
                
        except:
            messages.error(request, 'Resilt Not Edited')
            return JsonResponse('False',safe=False)
   


@login_required()
@csrf_exempt
def staff_student_result(request):
    user= request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session')

        student_obj = Student.objects.get(id=student_id)
        subject_obj = Subject.objects.get(id=subject_id)
        session_obj = SessionYear.objects.get(id=session_id)
        result = StudentResult.objects.filter(student_id=student_obj.id, subject_id=subject_obj.id,
                                              session_year_id=session_obj).exists()
        if result:

            result = StudentResult.objects.get(student_id=student_obj.id, subject_id=subject_obj.id,
                                               session_year_id=session_obj)

            result_data = {'id':result.id,'first_test': result.first_test, 'second_test': result.second_test}
            return JsonResponse(result_data, content_type='application/json', safe=False)
        else:
            return HttpResponse('False')


def delete_result(request):
    user= request.user
    if user.user_type != '2' or user.staff.current_position != 'teacher':
        return redirect(reverse('login'))
    else:
        if request.method == 'POST':
            student_id = request.POST.get('student_id')
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')

            student_obj = Student.objects.get(id=student_id)
            subject_obj = Subject.objects.get(id=subject_id)
            session_obj = SessionYear.objects.get(id=session_id)
            result_ext = StudentResult.objects.filter(student_id=student_obj.id, subject_id=subject_obj.id,
                                                session_year_id=session_obj).exists()
            if result_ext:
                result = StudentResult.objects.filter(student_id=student_obj.id, subject_id=subject_obj.id,
                                                session_year_id=session_obj)
                result.delete()
                return JsonResponse('deleted', safe=False)
            else:
               return JsonResponse('Not deleted', safe=False)
        else:
            return HttpResponse('Method Not Allowed')
            

        




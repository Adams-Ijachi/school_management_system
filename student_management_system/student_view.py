from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from student_management_system.forms import StudentProfileForm
from student_management_system.models import Student, AttendanceReport, NotificationReceiver, CustomUser, Subject, \
    Attendance, StudentResult, Class, SessionYear
from .pdf import render_to_pdf
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa
from io import BytesIO




@login_required
def home(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        user_obj = user.id

        student = Student.objects.get(admin=user_obj)
        notify = NotificationReceiver.objects.filter(user_id=user_obj).count(),
       
        try:
            student_class = student.grade.id
            subject_obj = Subject.objects.filter(grade=student_class).count()
            attendance_obj = AttendanceReport.objects.filter(student_id=student).count()
            attendance_present = AttendanceReport.objects.filter(student_id=student, status=True).count()

            attendance_absent = AttendanceReport.objects.filter(student_id=student, status=False).count()

            attendance_date =[]
            student_present_count = []
            student_absent_count = []

            attendance_data = AttendanceReport.objects.filter(student_id=student)
            for i in attendance_data:
                student_present = AttendanceReport.objects.filter(status=True, id=i.id).count()
                student_absent = AttendanceReport.objects.filter(status=False, id=i.id).count()
                student_date = i.attendance_id.attendance_date
                attendance_date.append(str(student_date))
                student_absent_count.append(student_absent)
                student_present_count.append(student_present)
            return render(request, 'student/student_home.html', {'attendance_obj': attendance_obj,
                                                                'attendance_present': attendance_present,
                                                                'attendance_absent': attendance_absent,
                                                                'attendance_date': attendance_date,
                                                                'student_present': student_present_count,
                                                                'student_absent': student_absent_count,
                                                                'subject_obj': subject_obj})
        except AttributeError: 
             return render(request, 'error/error-base.html')
      
    


@login_required
def view_attendance(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        student_id = user.student.id
        student = Student.objects.get(id=student_id)
        attendance = AttendanceReport.objects.filter(student_id=student)
        return render(request, 'student/view_attendance.html', {'attendance': attendance})


@login_required
def view_notification(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        user_id = request.user.id
        notification_obj = NotificationReceiver.objects.filter(user_id=user_id)
        return render(request, 'student/view_notification.html', {'notice': notification_obj})


@login_required
def read_notification(request, pk):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        request.session['message_id'] = pk
        message = NotificationReceiver.objects.get(id=pk)

        return render(request, 'student/read_notification.html', {'message_id': message})


@login_required
def student_edit_profile(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        form = StudentProfileForm()
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['username'].initial = user.username
        form.fields['address'].initial = user.student.address
        form.fields['profile_Image'].initial = user.student.profile_Image
        return render(request, 'student/edit_profile.html', {'form': form})


@login_required
def student_edit_profile_save(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = StudentProfileForm(request.POST, request.FILES)
            image = user.student.profile_Image
            if form.is_valid():
                user = CustomUser.objects.get(id=user.id)
                student = Student.objects.get(id=user.student.id)

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                address = form.cleaned_data["address"]
                profile_Image = form.cleaned_data['profile_Image']
                if not profile_Image:
                    profile_Image = image

                try:
                    user.last_name = last_name
                    user.first_name = first_name
                    user.username = username
                    student.address = address
                    student.profile_Image = profile_Image
                    student.save()

                    if password is not None and password != '':
                        user.set_password(password)
                    user.save()
                    if password:
                        return redirect(reverse('student_edit_profile'))
                    else:
                        messages.success(request, 'Student Added Successfully')
                        return redirect(reverse('student_edit_profile'))

                except:
                    messages.error(request, 'Profile Not Edited')
                    return redirect(reverse('student_edit_profile'))
            else:
                messages.error(request, 'Profile Not Edited')
                return redirect(reverse('student_edit_profile'))

@login_required
def student_session(request):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        sessions = SessionYear.objects.all()
        return render (request, 'student/result_session.html', {'session':sessions})



@login_required
def view_result(request, pk):
    user = request.user
    if user.user_type != '3':
        return redirect(reverse('login'))
    else:
        student_obj = Student.objects.get(id=user.student.id)
        session  = SessionYear.objects.get(id=pk)
        session_ext = student_result = StudentResult.objects.filter(student_id=student_obj, session_year_id=session).exists()
        if session_ext:
            student_result = StudentResult.objects.filter(student_id=student_obj,session_year_id=session)
            average = StudentResult.objects.filter(student_id=student_obj).annotate(prod= F('first_test') + F('second_test'))
            return render(request, 'student/view_result.html', {'student_result': student_result, 'average': average, 'key':pk})
        else:
            return HttpResponse('No Result Available')



class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        student_obj = Student.objects.get(id=user.student.id)
        pk = kwargs.get('pk')
        session = get_object_or_404(SessionYear, pk=pk)
        template_path = 'student/pdf.html'
        student_result = StudentResult.objects.filter(student_id=student_obj,session_year_id=session)
        average = StudentResult.objects.filter(student_id=student_obj).annotate(prod= F('first_test') + F('second_test'))
        context = {'student_result': student_result, 'average': average}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition']= 'filename:"report.pdf"'

        template = get_template(template_path)
        html= template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response
        )
        if pisa_status.err:
            return HttpResponse('bad')
        return response

       
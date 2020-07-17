from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from student_management_system.forms import ParentProfileForm
from student_management_system.models import Student, AttendanceReport, NotificationReceiver, CustomUser, Parent, \
    StudentResult


@login_required
def home(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        return render(request, 'parent/parent_home.html')


@login_required
def child_view_attendance(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        user_id = request.user.parent.id
        child = Student.objects.filter(parent=user_id)

        return render(request, 'parent/children_list.html', {'child': child})


@login_required
def get_attendance(request, pk):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        student = Student.objects.get(id=pk)
        attendance = AttendanceReport.objects.filter(student_id=student)
        return render(request, 'parent/view_attendance.html', {'attendance': attendance})


@login_required
def parent_view_notification(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        user_id = request.user.id
        notification_obj = NotificationReceiver.objects.filter(user_id=user_id).order_by('-id')
        return render(request, 'parent/view_notification.html', {'notice': notification_obj})


@login_required
def parent_read_notification(request, pk):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        request.session['message_id'] = pk
        message = NotificationReceiver.objects.get(id=pk)
        return render(request, 'parent/read_notification.html', {'message_id': message})


@login_required
def parent_edit_profile(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:

        form = ParentProfileForm()
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['username'].initial = user.username
        form.fields['address'].initial = user.parent.address
        form.fields['phone_number'].initial = user.parent.phone_number
        form.fields['profile_Image'].initial = user.parent.profile_Image
        return render(request, 'parent/edit_profile.html', {'form': form})


@login_required
def parent_edit_profile_save(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        if request.method != 'POST':
            return HttpResponse('Method Not Allowed')
        else:
            form = ParentProfileForm(request.POST, request.FILES)
            image = user.parent.profile_Image
            if form.is_valid():
                user = CustomUser.objects.get(id=user.id)
                parent = Parent.objects.get(id=user.parent.id)

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
                    parent.address = address
                    parent.profile_Image = profile_Image
                    parent.save()

                    if password is not None and password != '':
                        user.set_password(password)
                    user.save()
                    if password:
                        return redirect(reverse('parent_edit_profile'))
                    else:
                        messages.success(request, 'Profile Edited Successfully')
                        return redirect(reverse('parent_edit_profile'))

                except:
                    messages.error(request, 'Profile Not Edited')
                    return redirect(reverse('parent_edit_profile'))
            else:
                messages.error(request, 'Profile Not Edited')
                return redirect(reverse('parent_edit_profile'))


@login_required
def parent_view_result(request):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        user_id = request.user.parent.id
        child = Student.objects.filter(parent=user_id)
        return render(request, 'parent/view_result_list.html', {'child': child})


@login_required
def get_result(request, pk):
    user = request.user
    if user.user_type != '4':
        return redirect(reverse('login'))
    else:
        student_obj = Student.objects.get(id=pk)
        student_result = StudentResult.objects.filter(student_id=student_obj)
        average = StudentResult.objects.filter(student_id=student_obj).annotate(prod=F('first_test') + F('second_test'))

        return render(request, 'parent/view_result.html', {'student_result': student_result, 'average': average})

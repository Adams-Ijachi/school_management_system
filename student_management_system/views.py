
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse


from student_management_system.backends import EmailAuthentication
from student_management_system.forms import LoginForm
# Create your views here.


def loginPage(request):
    form = LoginForm()
    next_page = request.GET.get('next')
    return render(request, 'admin/login_page.html', {'form': form, 'next': next_page})


def LoginLogic(request):
    next = request.POST.get('next')
    if request.method != 'POST':
        return HttpResponse('<h1>Method Not Allowed</h1>')

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = EmailAuthentication.authenticate(request,  username=email,
                                                    password=password)
            if user is not None:
                login(request, user)
                if user.user_type == '1':
                    if next != 'None' and next:
                        return redirect(next)
                    else:
                        return redirect(reverse('admin_home'))
                elif user.user_type == '2':
                    if next != 'None' and next:
                        return redirect(next)
                    return redirect(reverse('staff_home'))
                elif user.user_type == '3':
                    if next != 'None' and next:
                        return redirect(next)
                    return redirect(reverse('student_home'))
                elif user.user_type == '4':
                    if next != 'None' and next:
                        return redirect(next)
                    return redirect(reverse('parent_home'))
                else:
                    messages.error(request, 'invalid Login Details')
                    return redirect(reverse('login'))
            else:
                messages.error(request, 'invalid Login Details')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'invalid Login Details')
            return redirect(reverse('login'))


def LogoutUser(request):
    logout(request)
    return redirect(reverse('login'))





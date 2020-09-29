from django.test import TestCase

# Create your test
class StaffEditResult(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user == 'AnonymousUser' or user.user_type != '2' or user.staff.current_position != 'teacher':
            print('k')
        else:
            staff_id = request.user.staff.id
            print('k')
            form = EditResultForm(staff_id=staff_id)
            print('k1')
            class_ext = Class.objects.filter(form_master=staff_id).exists()
            print('k6')

            if class_ext:
                return render(request, 'staff/edit_result.html', {'form': form})
                print('k4')
            else:
                return HttpResponse('Not A Form Master Cant Add or Edit Result')
                print('k3')

    def post(self, request,  *args, **kwargs):
        staff_id = request.user.staff.id
        print('ii')

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
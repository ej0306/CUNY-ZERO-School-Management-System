from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from courses.models import Session, TakenCourse, Result
from users.models import Student
from .forms import GraduationApplicationForm, AcceptApplication
from .models import GraduationApplication


# Create your views here.
@login_required()
def apply_for_graduation(request):
    if request.method == 'POST':
        form = GraduationApplicationForm(request.POST)

        if GraduationApplication.objects.filter(student__user_id=request.user.id, pending=True).exists():
            messages.error(request, 'You have already submitted an application previously.')
            return redirect('graduation-apply')

        if form.is_valid():
            app = form.save(commit=False)
            app.student = Student.objects.get(user__pk=request.user.id)
            app.save()
            messages.success(request, f'Your Application has been submitted and is pending for review by a registrar!')
            return redirect('graduation-apply')
    else:
        form = GraduationApplicationForm()
    context = {
        'title': 'Apply for Graduation',
        'form': form
    }
    return render(request, 'graduation/apply_for_graduation.html', context)


@login_required
def graduation_applications(request):
    if not request.user.is_registrar:
        raise PermissionDenied()

    context = {
        'applications': GraduationApplication.objects.all()
    }

    return render(request, 'graduation/graduation_applications_list.html', context)


@login_required
def graduation_application_details(request, pk):
    if not request.user.is_registrar:
        raise PermissionDenied()

    application = GraduationApplication.objects.filter(id=pk).first()

    student = Student.objects.get(user__pk=application.student.user.id)
    current_session = Session.objects.get(is_current_session=True)
    courses = TakenCourse.objects.filter(student__user__pk=application.student.user.id)
    result = Result.objects.filter(student__user__pk=application.student.user.id)
    current_semester_grades = {}

    context = {
        "courses": courses,
        "result": result,
        "student": student,
        "current_session": current_session,
    }

    if request.method == 'POST':
        form = AcceptApplication(request.POST)

        if form.data.get('decision') == 'Y':
            application.approved = True
            application.pending = False
            application.save()

            student.graduation_class = application.graduation_class
            student.graduation_date = application.graduation_class.graduation_date
            student.save()

            # TO DO - notify about decision
            return redirect('grad_applications')
        else:
            application.rejected = True
            application.pending = False
            application.save()

            # TO DO - warning/notify about decision
            return redirect('grad_applications')
    else:
        form = AcceptApplication()

    context.update({
        'application': application,
    })

    if application.pending:
        context.update({
            'form': form,
        })

    return render(request, 'graduation/graduation_application_details.html', context)

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import StudentApplicationForm, InstructorApplicationForm, AcceptApplication, EnrollmentApplication, LoginForm, UserCreation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from users.models import Instructor, Student, User
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, FileResponse
from CUNYzero import settings
import os

from courses.models import Classes, TakenCourse 

# Create your views here.
def register_student(request):
    if request.user.is_authenticated:
        return redirect(profile)

    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)

        # do something if form is completed successfully
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Application has been submitted and is pending for review by a registrar!')
            return redirect('login')
    else:
        form = StudentApplicationForm()
    return render(request, 'users/registerStudent.html', {'form': form})


def register_instructor(request):
    if request.user.is_authenticated:
        return redirect(profile)

    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST, request.FILES)

        # do something if form is completed successfully
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Application has been submitted and is pending for review by a registrar!')
            return redirect('login')
    else:
        form = InstructorApplicationForm()
    return render(request, 'users/registerInstructor.html', {'form': form})


@login_required
def profile(request):
    courses = Classes.objects.filter(allocated_course__instructor__pk = request.user.id)
    taken_course = TakenCourse.objects.filter(student__user__pk = request.user.id)


    context = {
        "courses": courses,
        "taken_course": taken_course,
    }
    return render(request, 'users/profile.html', context)


@login_required
def enrollment_applications(request):

    context = {
        'applications': EnrollmentApplication.objects.all()
    }
    if not request.user.is_registrar:
        raise PermissionDenied()

    return render(request, 'users/enrollment_applications.html', context)


@login_required
def enrollment_application_details(request, pk):
    if not request.user.is_registrar:
        raise PermissionDenied()

    application = EnrollmentApplication.objects.filter(id=pk).first()
    context = {}

    if request.method == 'POST':
        form = AcceptApplication(request.POST)

        if form.data.get('decision') == 'Y':

            if form.data.get('reason') == '' and application.gpa <= 3.0 and application.student_application:
                messages.error(request, 'Please provide a justification for this decision.')
                return render(request, 'users/enrollmentapplication_detail.html', {'form': form, 'application': application})

            application.status_approved = True
            application.status_pending = False

            new_username = create_username(application.first_name, application.last_name, 0)
            new_user = User.objects.create(username=new_username, email=application.email, new_user=True)

            new_user.first_name = application.first_name
            new_user.last_name = application.last_name
            new_user.m_initial = application.m_initial
            new_user.birth_date = application.birth_date
            new_user.phone_number = application.phone_number
            new_user.street_address = application.street_address
            new_user.city = application.city.capitalize()
            new_user.state = application.state.upper()
            new_user.zip_code = application.zip_code

            application_type = ''
            if application.student_application:
                new_user.is_student = True
                application_type = 'student'
            elif application.Instructor_application:
                new_user.is_instructor = True
                application_type = 'instructor'

            raw_pwd = User.objects.make_random_password(length=10, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
            new_user.set_password(raw_pwd)
            new_user.save()

            if application.student_application:
                student = Student.objects.create(user=new_user)
                student.sc_name = application.sc_name
                student.sc_city = application.sc_city
                student.sc_state = application.sc_state
                student.graduation_date = application.graduation_date
                student.gpa = 0.0
                student.semester = "First"
                student.transcript = application.transcript
                student.save()
            elif application.Instructor_application:
                instructor = Instructor.objects.create(user=new_user)
                instructor.resume = application.resume
                instructor.save()

            notify_accepted_applicant(new_user.id, raw_pwd, application_type)
            application.save()

            return redirect('enrollment_applications')
        else:
            if form.data.get('reason') == '' and application.gpa > 3.0 and application.student_application:
                messages.error(request, 'Please provide a justification for this decision.')
                return render(request, 'users/enrollmentapplication_detail.html', {'form': form, 'application': application})

            application.status_rejected = True
            application.status_pending = False
            application.save()

            application_type = ''
            if application.student_application:
                application_type = 'student'
            elif application.Instructor_application:
                application_type = 'instructor'

            notify_rejected_applicant(application.id, application_type, form.data.get('reason'))

            return redirect('enrollment_applications')
    else:
        if application.student_application:
            if application.gpa > 3.0:
                form = AcceptApplication(initial={'decision': 'Y'})
            else:
                form = AcceptApplication(initial={'decision': 'N'})
        else:
            form = AcceptApplication()

    context.update({
        'application': application,
    })

    if application.status_pending:
        context.update({
            'form': form,
        })

    return render(request, 'users/enrollmentapplication_detail.html', context)


def create_username(f_name, l_name, cnt):
    new_username = f_name[0] + l_name + str(cnt)
    if User.objects.filter(username=new_username).exists():
        create_username(f_name, l_name, cnt+1)
    else:
        return str(new_username)


def notify_accepted_applicant(user_id, raw_password, application_type):
    user_object = User.objects.get(id=user_id)
    msg = 'Dear ' + (user_object.first_name + " " + user_object.last_name).upper() + ", \n\n" + \
          "We are pleased to tell you that your " + application_type + " application has been approved.\n" \
          "Below, you will find your account information: \n\n" \
          "Username: " + user_object.username + "\n" + \
          "Password: " + raw_password + "\n" + \
          "ID: " + str(user_object.id) + "\n\n Best regards,\n The CUNYZero team"
    send_mail(
        subject='CUNYZero - Enrollment Decision',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_object.email])


def notify_rejected_applicant(application_id, application_type, reason):
    application_obj = EnrollmentApplication.objects.get(id=application_id)
    msg = 'Dear ' + (application_obj.first_name + " " + application_obj.last_name).upper() + ", \n\n" + \
          "We are sorry to inform you that your " + application_type + " application has been rejected.\n\n" \
          "The reason for rejection is: \n\n"
    if not reason == '':
        msg += reason
    msg += "\n\n Best regards,\n The CUNYZero team"
    send_mail(
        subject='CUNYZero - Enrollment Decision',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[application_obj.email])


@login_required
def student_list(request):
    "List of all student"
    students = Student.objects.all()
    user_type = "student"
    context = {
        "students": students ,
        "user_type": user_type,
    }
    return render (request, 'users/student_list.html', context)


@login_required
def instructor_list(request):
    "List of all student"
    instructors = Instructor.objects.all()
    user_type = "instructor"
    context = {
        "instructors": instructors,
        "user_type": user_type,
    }
    return render(request, 'users/instructor_list.html', context)


class LoginUser(LoginView):
    template_name = 'users/login.html'
    login_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.new_user:
            return reverse(change_password)

        return super().get_success_url()


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.new_user = False
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('general-home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required()
def create_user(request):
    if not request.user.is_superuser:
        return redirect('general-home')

    form = UserCreation()

    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('general-home')

    return render(request, 'users/user_creation.html', {'form': form})


# open pdf file from admin site
def show_pdf(request, file_name):
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def show_application_file(request, pk, file_name):
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
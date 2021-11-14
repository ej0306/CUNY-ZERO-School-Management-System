from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegisterForm, InstructorRegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)

        # do something if form is completed successfully
        if form.is_valid():

            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/registerStudent.html', {'form': form})


def register_instructor(request):
    if request.method == 'POST':
        form = InstructorRegisterForm(request.POST, request.FILES)

        # do something if form is completed successfully
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = InstructorRegisterForm()
    return render(request, 'users/registerInstructor.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


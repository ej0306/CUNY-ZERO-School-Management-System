
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpRequest, JsonResponse
from django.urls.base import reverse
from courses.models import Course, Classes, RepeatingStudent, ReviewClasses, Session, TakenCourse, Result
from users.models import Student
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import *
from django.contrib.auth.decorators import permission_required



# Create your views here

#-----------------------------------------------------------------------------------------#
#                          Courses/Classes Related Views                                  #
#-----------------------------------------------------------------------------------------#

# View for the courses offered page
@login_required
def courses_offered(request):
    model = Course
    #Show all courses
    courses = Course.objects.order_by('title')
    context = {'courses' : courses}
    return render(request, 'courses/courses_offered.html', context)


@login_required
def list_classes(request):
    #Show all Classses
    classes = Classes.objects.all()
    context = {'classes' : classes}
    return render(request, 'courses/classes_list.html', context)


@login_required
def course_allocation_view(request):
    classes = Classes.objects.all()
    context = {'classes' : classes}
    return render(request, 'courses/course_allocation.html', context)

    
@login_required
def add_score(request):
    """ Show the first page where the instructor have to select one of its course."""
    current_session = Session.objects.get(is_current_session=True)
    classes = Classes.objects.filter(allocated_course__instructor__pk = request.user.id) #Check 
    context= { 
        "classes" : classes ,
        "current_session": current_session,

    }
    return render(request, "courses/add_score.html", context)


@login_required
def add_score_for(request, id):
    """ Show the page where an instructor will grade students enrolled in a 
        specific class """
    current_session = Session.objects.get(is_current_session=True)
    if request.method  == 'GET':
        courses = Classes.objects.filter(allocated_course__instructor__pk = request.user.id) #Check
        course = Classes.objects.get(pk=id)
        students = TakenCourse.objects.filter(classes__allocated_course__instructor__pk = request.user.id).filter(classes__id = id) #Check
        context = {
            "courses": courses,
            "course ": course,
            "students": students,
            "current_session": current_session,

        }
        return render(request, "courses/add_score_for.html", context)

    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None) #remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)      # gather all the all students id (i.e the keys) in a tuple

        for s in range(0,len(ids)):      # iterate over the list of student ids gathered above
            student = TakenCourse.objects.get(id = ids[s])
            courses = Classes.objects.filter(semester = student.student.semester)
            total_unit_semester = 0
            for i in courses:
                if i ==courses.count():
                    break
                else:
                    total_unit_semester += int(i.credit)

            score = data.getlist(ids[s])
            ca = score[0]
            exam = score[1]
            obj = TakenCourse.objects.get(pk =ids [s])
            obj.ca = ca
            obj.exam = exam
            obj.total = obj.get_total(ca = ca, exam = exam)
            obj.grade = obj.get_grade(ca=ca, exam=exam)
            obj.comment = obj.get_comment(obj.grade)
            obj.save()

        messages.success(request, 'Succesfully Recorded!')

        return HttpResponseRedirect(reverse_lazy('courses:add_score_for', kwargs = {'id': id }))
    return HttpResponseRedirect(reverse_lazy('courses:add_score_for', kwargs = {'id': id }))


       

# Handles the class search results
@login_required
def class_search(request):        
    if request.method == 'GET': 
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query:
            lookups =  ( 
                Q(semester__icontains= query) | Q(class_id__icontains= query) | 
                Q(year__icontains= query) |  Q(days_and_time__icontains= query) | 
                Q(course__course_name__icontains= query) | Q(course__title__icontains= query)
              )
                    
            # lookups2= Q(course_name__icontains= query)| Q(title__icontains= query)
            results = Classes.objects.filter(lookups).distinct()
            # results2 = Course.objects.filter(lookups2).distinct()

            context = {'results': results,  'submitbutton': submitbutton}

            return render(request, 'courses/class_search.html', context)

        else: 
            return render(request, 'courses/class_search.html')

    else:
         return render(request, 'courses/class_search.html')



def description(request):
    return render(request, 'courses/course_description.html')

@login_required
#@permission_required('is_student')
def course_registration(request):
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None) # remove csrf_token
        for key in data.keys():
            ids= ids + (str(key),)
        for s in range (0, len(ids)):
            student = Student.objects.get(user__pk = request.user.id)
            classes = Classes.objects.get(pk = ids[s])

            obj = TakenCourse.objects.create(student = student, classes = classes)
            obj.save()
            messages.success(request, 'Courses Registered Successfully!')
        return redirect('courses:course_registration')
    
    else:
        student = Student.objects.get(user__pk= request.user.id)
        taken_courses = TakenCourse.objects.filter(student__user__id= request.user.id)
        t = ()
        for i in taken_courses:
            t+= (i.classes.pk,)
        classes = Classes.objects.filter(semester = student.semester).exclude(id__in= t)
        all_classes = Classes.objects.filter(semester = student.semester)

        no_course_is_registered = False
        all_courses_are_registered = False

        registered_classes = Classes.objects.filter(semester = student.semester).filter(id__in=t)
        if registered_classes.count() ==0:
            no_course_is_registered = True
        
        if registered_classes.count() == all_classes.count():
            all_courses_are_registered = True


        total_first_semester_unit = 0
        total_second_semester_unit = 0
        total_registered_unit = 0

        for i in classes:
            if i.semester =="First":
                total_first_semester_unit+= int(i.credit)
            if i.semester == "Second":
                total_second_semester_unit+=int(i.credit)
           

        for i in registered_classes:
            total_registered_unit += int(i.credit)

        context = {
            
            "no_course_is_registered" : no_course_is_registered,
            "all_courses_are_registered": all_courses_are_registered,
            "classes": classes,
            "registered_classes": registered_classes,
            "student": student,
            "total_first_semester_unit": total_first_semester_unit,
            "total_second_semester_unit": total_second_semester_unit,
            "total_registered_unit": total_registered_unit,
            
            }
        return render(request, 'courses/course_registration.html', context)



    
@login_required
def course_drop(request):
    if request.method =='POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None) # remove csrf_token
        for key in data.keys():
            ids = ids + (str (key),)
        for s in range (0, len(ids)):
            student = Student.objects.get(user__pk = request.user.id)
            classes = Classes.objects.get(pk = ids[s])
            obj = TakenCourse.objects.get(student = student, classes = classes)
            obj.delete()
            messages.success(request, 'Successfully Dropped!')
        return redirect('courses:course_registration')


@login_required
def view_result(request):
    student = Student.objects.get(user__pk=request.user.id)
    current_session = Session.objects.get(is_current_session=True)
    courses = TakenCourse.objects.filter(student__user__pk=request.user.id)
    result = Result.objects.filter(student__user__pk=request.user.id)
    current_semester_grades = {}

    previousCGPA = 0
  

    context = {
            "courses": courses, 
            "result":result, 
            "student": student, 
            "previousCGPA": previousCGPA,
            "current_session": current_session,
            }

    return render(request, 'courses/view_results.html', context)



@login_required
def repeat_list(request):
    students = RepeatingStudent.objects.all()
    return render(request, 'courses/repeaters.html', {"students": students})


def first_class_list(request):
    students = Result.objects.filter(cgpa__gte=3.5)
    return render(request, 'courses/first_class_students.html', {"students": students})



#-----------------------------------------------------------------------------------------#
#                                   Reviews Classes Views                                 #
#-----------------------------------------------------------------------------------------#
@login_required
def review_list(request):
    latest_review_list = ReviewClasses.objects.order_by('-date_added')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)

@login_required
def review_detail(request, review_id):
    review = get_object_or_404(ReviewClasses, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})

@login_required
def course_list(request):
    course_list = Classes.objects.all()
    context = {'course_list':course_list}
    return render(request, 'reviews/course_list.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Classes, pk=course_id)
    form = ReviewForm()
    return render(request, 'reviews/course_detail.html', {'course': course, 'form': form})


@login_required
def add_review(request, course_id):
    course = get_object_or_404(Classes, pk=course_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rate = form.cleaned_data['rate']
        review = form.cleaned_data['review']
        owner = request.user.student

        reviews = ReviewClasses()
        reviews.course = course
        reviews.rate = rate
        reviews.owner = owner
        reviews.review = review
        reviews.date_added = datetime.datetime.now()
        reviews.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('courses:course_detail', args=(course.id,)))

    return render(request, 'reviews/review_detail.html', {'course': course, 'form': form})



def best_rated_classes(request):
    classes = ReviewClasses.objects.all()
    return render(request, 'reviews/best_rated_classes.html', {'classes': classes})


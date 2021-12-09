
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import OneToOneField
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpRequest, JsonResponse
from django.urls.base import reverse
from courses.models import *
from users.models import Instructor, Student
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

    class_dict = {}
    for i in classes:
        class_dict.update({i.get_cur_capacity(): i})

    context = {"classes" : classes, "class_dict": class_dict,}
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
    classes = Classes.objects.filter(instructor__pk = request.user.id) #Check 
    context= { 
        "classes" : classes ,
        "current_session": current_session,

    }
    return render(request, "courses/add_score.html", context)


@login_required
def add_score_for(request, id):
    """ Show the page where an instructor will grade students enrolled in a 
        specific class """
   
    course = Classes.objects.get(pk = id)
    current_session = Session.objects.get(is_current_session=True)
    if request.method  == 'GET':
        courses = Classes.objects.filter(instructor__pk = request.user.id) #Check
        
       
        students = TakenCourse.objects.filter(classes__instructor__pk = request.user.id).filter(classes__id = id) #Check
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


@login_required
def wait_list_view(request):
    #  wait_list = WaitList.objects.filter(student__pk = request.user.id)
    #         context = {"wait_list": wait_list}
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None) # remove csrf_token
       
        for key in data.keys():
            ids = ids + (str(key),)

        wait_list = WaitList.objects.filter(instructor__pk = request.user.id)
        
        wait_list_dict = {}
        for i in wait_list:
            wait_list_dict.update({i.student.user.id : i.course})

        for s in range (0, len(ids)):
            student_id = 0
            course = Classes.objects.get(pk = ids[s])

            for x, y in wait_list_dict.items():
               if y == course:
                   student_id = x

            
            student = Student.objects.get(user__pk = student_id)
            # student =None
            
            obj = TakenCourse.objects.create(student = student, classes = course)
            obj.save()
            

            d_obj = WaitList.objects.get(student = student, course = course)
            d_obj.delete()
            messages.success(request, 'Student Added To Wait List Succesffully!')
           
        return redirect('courses:wait_list_view')

    else: 
        wait_list = WaitList.objects.filter(instructor__pk = request.user.id)
        context = {"wait_list": wait_list}

        return render(request, "courses/wait_list.html", context)






       

# Handles the class search results
@login_required
def class_search(request):        
    if request.method == 'GET': 
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query:
            lookups = (
                Q(semester__icontains=query) | Q(class_id__icontains=query) |
                Q(year__icontains=query) | Q(days__icontains=query) | Q(start_time__icontains=query) |
                Q(end_time__icontains=query) | Q(instructor__user__last_name__icontains=query) |
                Q(course__course_name__icontains=query) | Q(course__title__icontains=query))
# =======
#             lookups =  (
#                 Q(semester__icontains= query) | Q(class_id__icontains= query) |
#                 Q(year__icontains= query) |   Q(days__icontains= query) |  Q(instructor__user__last_name__icontains= query) |
#                 Q(course__course_name__icontains= query) | Q(course__title__icontains= query)
# >>>>>>> merge-dec-7
#               )
                    
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
    time_dict = {}
    current_session = Session.objects.get(is_current_session=True)
    current_period = current_session.current_period

    if request.method == 'POST':
        if current_period == "Course Registration Period":
            ids = ()
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken', None) # remove csrf_token


            
            is_full = False
            time_conflict = False
            another_section = False

            for key in data.keys():
                ids= ids + (str(key),)

            
            classes = Classes.objects.all()
            taken_courses = TakenCourse.objects.filter(student__user__id= request.user.id)
            for s in range (0, len(ids)):
                student = Student.objects.get(user__pk = request.user.id)
                course = Classes.objects.get(pk = ids[s])
            

                #Check if the class reached full capacity yet. 
                course_cur_cap = course.get_cur_capacity()

                check_waitList = WaitList.objects.filter(student = student, course = course)

            
                # Put the start and end time of the student current class in a dictionary. 
                for i in taken_courses:
                    time_dict.update({i.classes.start_time : i.classes.end_time})
                # for i in classes:
                #     time_dict.update({i.start_time : i.end_time})

                if course_cur_cap == course.full_capacity:
                    messages.warning(request, "Sorry you can't register for this class! Its full!" )
                    #Check if the student is already in the wait list for the class. 

                    if  check_waitList:
                        messages.warning(request, "You are already in the wait list for this class!")
                        messages.warning(request, "We ask of you to be patient!")
                    else:
                        # Put the student in a wait list
                        obj = WaitList.objects.create(student = student, course = course)
                        obj.save()
                        messages.warning(request, "You will be placed on a wait list!")

                else: 
                    for i in classes:
                        #Check if the classes have the same days. 
                        if i.days == course.days and i.class_id != course.class_id:

                            #Check for time conflict
                            for x, y in time_dict.items():
                                if x <= course.start_time <= y:
                                    time_conflict = True
                                    messages.warning(request, "Sorry! There is a time conflict with one of your classes!")
                                    break
                                
                                elif x <= course.end_time <= y:
                                    time_conflict = True
                                    messages.warning(request, "Sorry! There is a time conflict with one of your classes!")
                                    break
                                else: 
                                    time_conflict = False
                        
                    for i in taken_courses:
                        if i.classes.course.course_name == course.course.course_name:
                            messages.warning(request, "Sorry! are already enrolled in a section of this class!")
                            another_section = True
                        

                        
                    # Update time_dict with times of the newly added classes
                
                    if time_conflict is False and another_section is False:
                        time_dict.update({course.start_time : course.end_time})
                        obj = TakenCourse.objects.create(student = student, classes = course)
                        obj.save()
                        messages.success(request, 'Courses Registered Successfully!')
        else:
            messages.warning(request, " You are not allowed to register for classes at this time")

        return redirect('courses:course_registration')
    
    else:
        student = Student.objects.get(user__pk= request.user.id)
        taken_courses = TakenCourse.objects.filter(student__user__id= request.user.id)
        wait_list = WaitList.objects.filter(student__pk = request.user.id)
       
        t = ()
        
        for i in taken_courses:
            t+= (i.classes.pk,)
            
        classes = Classes.objects.filter(semester = student.semester).exclude(id__in= t)
        all_classes = Classes.objects.filter(semester = student.semester)

        no_course_is_registered = False
        all_courses_are_registered = False

        registered_classes = Classes.objects.filter(semester = student.semester).filter(id__in=t)
        # registered_classes = TakenCourse.objects.filter(student__pk = request.user.id)
        if registered_classes.count() ==0:
            no_course_is_registered = True
        
        if registered_classes.count() == all_classes.count():
            all_courses_are_registered = True


        total_first_semester_unit = 0
        total_second_semester_unit = 0
        total_registered_unit = 0
        
       
        
        # a dictionaty that have the current capacity as key and the class object as value
        class_dict = {}
        for i in classes:
            if i.semester =="First":
                total_first_semester_unit+= int(i.credit)
            if i.semester == "Second":
                total_second_semester_unit+=int(i.credit)
            
            class_dict.update({i.get_cur_capacity(): i})
         
       
           

        taken_class_dict = {}
        for i in registered_classes:
            total_registered_unit += int(i.credit)
            taken_class_dict.update({i.get_cur_capacity(): i})

            
        context = {
            
            "no_course_is_registered" : no_course_is_registered,
            "all_courses_are_registered": all_courses_are_registered,
            "classes": classes,
            "registered_classes": registered_classes,
            "student": student,
            "total_first_semester_unit": total_first_semester_unit,
            "total_second_semester_unit": total_second_semester_unit,
            "total_registered_unit": total_registered_unit,
            "class_dict": class_dict,
            "taken_class_dict": taken_class_dict,
            "wait_list": wait_list,
            "current_session": current_session,
            "current_period": current_period,
            
            
            }
        return render(request, 'courses/course_registration.html', context)



    
@login_required
def course_drop(request):
    current_session = Session.objects.get(is_current_session=True)
    current_period = current_session.current_period
    if request.method =='POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None) # remove csrf_token
        for key in data.keys():
            ids = ids + (str (key),)
        for s in range (0, len(ids)):
            student = Student.objects.get(user__pk = request.user.id)
            classes = Classes.objects.get(pk = ids[s])

            obj = TakenCourse.objects.get(student=student, classes=classes)

            if Session.objects.filter(is_current_session=True).first().is_class_running_period() or Session.objects.filter(is_current_session=True).first().is_grading_period():
                obj.dropped = True
                obj.grade = 'W'
                obj.save()
                messages.warning(request, 'Successfully dropped with grade W')
                if TakenCourse.objects.filter(student__user_id=request.user.id, dropped=True, classes__session__is_current_session=True).count() == TakenCourse.objects.filter(student__user_id=request.user.id, classes__session__is_current_session=True).count():
                    u = Student.user.objects.filter(user_id=request.user.id).first().is_suspended = True
                    u.save()
            else:
                obj.delete()
                messages.success(request, 'Successfully Dropped!')


        return redirect('courses:course_registration')


@login_required
def view_result(request):
    student = Student.objects.get(user__pk=request.user.id)
    # current_session = Session.objects.get(is_current_session=True)
    current_session = Session.objects.all()
    courses = TakenCourse.objects.filter(student__user__pk=request.user.id)
    result = Result.objects.filter(student__user__pk=request.user.id)
    current_semester_grades = {}

    previousCGPA = 0
    
    if current_session:
        current_session = Session.objects.get(is_current_session=True)
        context = {
                "courses": courses, 
                "result":result, 
                "student": student, 
                "previousCGPA": previousCGPA,
                "current_session": current_session,
                }
        return render(request, 'courses/view_results.html', context)
    else: 
        messages.warning(request, "There is no active session right now!")

    return render(request, 'courses/view_results.html')



@login_required
def repeat_list(request):
    students = RepeatingStudent.objects.all()
    return render(request, 'courses/repeaters.html', {"students": students})


def first_class_list(request):
    students = Result.objects.filter(cgpa__gte=3.5)
    return render(request, 'courses/first_class_students.html', {"students": students})


@login_required
def add_class(request):
    if not (request.user.is_registrar or request.user.is_superuser):
        return redirect('courses:list_classes')

    if request.method == 'POST':
        form = ClassSetUp(request.POST)
        if form.is_valid():
            new_class = form.save()
            new_class.current_capacity = 0
            new_class.class_id = new_class.id
            new_class.save()

            ca = CourseAllocation.objects.filter(instructor__user__id__iexact=new_class.instructor.user_id)

            if ca.exists():
                ca = ca.first()
                ca.courses.add(new_class)
                ca.save()
            else:
                ca = CourseAllocation.objects.create(instructor=new_class.instructor, session=Session.objects.filter(is_current_session=True).first())
                ca.save()

            return redirect('courses:list_classes')
    else:
        form = ClassSetUp()

    return render(request, 'courses/add_class.html', {'form': form, 'title': 'Add Class'})


@login_required
def add_course(request):
    if not (request.user.is_registrar or request.user.is_superuser):
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = CreateCourse(request.POST)
        if form.is_valid():
            new_course = form.save()
            new_course.save()
            return redirect('courses:courses_offered')
    else:
        form = CreateCourse()

    return render(request, 'courses/add_course.html', {'form': form, 'title': 'Create Course'})


@login_required()
def set_up_session(request):
    if not (request.user.is_registrar or request.user.is_superuser):
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = SetUpSession(request.POST)
        if form.is_valid():
            new_session = form.save()
            new_session.save()
            return redirect('courses:academic_sessions_list')
    else:
        form = SetUpSession()

    return render(request, 'courses/set_up_session.html', {'form': form, 'title': 'Set Up Academic Session'})


@login_required()
def sessions_list(request):
    if not (request.user.is_registrar or request.user.is_superuser):
        return redirect('courses:course_list')
    sessions = Session.objects.all()

    return render(request, 'courses/academic_sessions_list.html', {'sessions': sessions})


@login_required
def session_details(request, pk):
    s = Session.objects.filter(id=pk)

    if not s.exists():
        raise Http404
    else:
        s = s.first()
        csup = s.is_class_set_up_period()
        crp = s.is_course_registration_period()
        rp = s.is_class_running_period()
        gp = s.is_grading_period()

    context = {
        'session': s,
        'set_up_p': csup,
        'reg_p': crp,
        'run_p': rp,
        'grad_p': gp,
    }
    return render(request, 'courses/session_details.html', context)


# -----------------------------------------------------------------------------------------#
#                                   Reviews Classes Views                                 #
# -----------------------------------------------------------------------------------------#


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

    current_session = Session.objects.get(is_current_session=True)
    current_period = current_session.current_period

    if current_period != "Grading Period":
       
        has_bad_word = False

        bad_words = [
            "fuck" , "fuck!" , "fucking", "sucks", "asshole",
            "dick", "motherfucker", "ass", "pussy",
            "faggot", "bitch", "cunt", "whore",
            "suck", "sucks!", 
            "fuck!!" , "fuck!" , "fucking!", "sucks!", "asshole!",
            "dick!", "motherfucker!", "ass!", "pussy!",
            "faggot!", "bitch!", "cunt!", "whore!",
            "suck!", "sucks!", 
            "fuck." , "fuck.!" , "fucking.", "sucks.", "asshole.",
            "dick.", "motherfucke.r", "ass.", "pussy.",
            "faggot.", "bitch.", "cunt.", "whore.",
            "suck.", "sucks.!", "shit", 
        ]

        bad_words_dict = {}
        for i in  range ( 0 , len(bad_words)):
            temp = []
            for j in range ( 0, len(bad_words[i])):
                temp.append("*")
            str_temp = ' '.join(temp)
            bad_words_dict.update({bad_words[i]: str_temp})




        if form.is_valid():
            rate = form.cleaned_data['rate']
            review = form.cleaned_data['review']
            owner = request.user.student

            list_review = review.split()
            
            taboo_word_ct = 0
            for i in range(0, len(list_review)):
                word = list_review[i]
                for x, y in bad_words_dict.items():
                    if word.lower() == x:
                        taboo_word_ct += 1
                        list_review[i]= y

            censored_review = "  ".join(list_review)

            check_warning = WarningCount.objects.all()

            if 1 <= taboo_word_ct <= 2:
                reviews = ReviewClasses()
                reviews.course = course
                reviews.rate = rate
                reviews.owner = owner
                reviews.review = censored_review
                reviews.non_censored = review
                reviews.date_added = datetime.datetime.now()
                reviews.save()
                messages.warning(request, "Taboo words detected (1 warning). Please remain respectfull!")

                if check_warning is None:
                    obj = WarningCount()
                    obj.student= request.user.student
                    obj.count = "1"
                    obj.save()
                else:

                    for i in check_warning:
                        if i.student == request.user.student:
                            count = int(i.count) + 1
                            obj = WarningCount.objects.filter(student = request.user.student).update(count = str(count))
                            # obj.save()

            
            elif taboo_word_ct >= 2: 
                messages.warning(request, "Too many taboo words. This count as 2 warning!")
                if check_warning is None:
                    obj = WarningCount.objects.create(student = request.user.student, count = "2")
                    obj.save()
                else:
                    for i in check_warning:
                        if i.student == request.user.student:
                            count = int(i.count) + 2
                            obj = WarningCount.objects.filter(student = request.user.student).update(count = str(count))
                            # obj.save()

            else: 
                reviews = ReviewClasses()
                reviews.course = course
                reviews.rate = rate
                reviews.owner = owner
                reviews.review = censored_review
                reviews.date_added = datetime.datetime.now()
                reviews.save()


            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('courses:course_detail', args=(course.id,)))

        return render(request, 'reviews/review_detail.html', {'course': course, 'form': form})
    else:
        messages.warning(request, "You are not allowed to post reviews at this time!")
        course_list = Classes.objects.all()
        context = {'course_list':course_list}
        return render(request, 'reviews/course_list.html', context)



def best_rated_classes(request):
    classes = ReviewClasses.objects.all()
    return render(request, 'reviews/best_rated_classes.html', {'classes': classes})







def send_warnings_auto(request):
    taken_courses = TakenCourse.objects.all()
    classes = Classes.objects.all()
    students = Student.objects.all()
    instructors = Instructor.objects.all()
    current_session = Session.objects.get(is_current_session=True)
    current_period = current_session.current_period

    if request.method == 'POST':

        if current_period == "Class Running Period":

            for i in students:
                courses = TakenCourse.objects.filter(student__pk = i.id)
                number_of_courses = len(courses)
                if number_of_courses <=2:
                    obj = AutomaticWarning()
                    obj.user = i 
                    obj.warning_text = "ATTENTION! you only registered for two courses this semester. The registration period ended!"
                    obj.date_added = DateTimeField.auto_created
                    obj.save

            for i in classes:
                if i.get_currrent_capacity <= 5:
                    obj = AutomaticWarning()
                    obj.user = i.instructor
                    obj.warning_text = "ATTENTION! Your class was cancelled due the two little number of students!"
                    obj.date_added = DateTimeField.auto_created
                    obj.save()

        return redirect('courses:send_warnings_auto')

    else:
        all_warning = AutomaticWarning.objects.all()
        your_warning = AutomaticWarning.objects.filter(user__pk = request.user.id)

        context = {
            "all_warning": all_warning,
            "your_warning": your_warning,
        }

        return render(request, 'courses/warning.html', context)

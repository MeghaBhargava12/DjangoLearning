from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Category, Course, Student, Instructor,Order
from .forms import InterestForm,OrderForm,LoginForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.utils import timezone

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            user = authenticate(request,username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    utc_now = datetime.now(timezone.utc)
                    eastern = timezone.get_fixed_timezone(timedelta(hours=-5))
                    eastern_time = utc_now.astimezone(eastern)
                    request.session['last_login_info'] = eastern_time.strftime('%Y-%m-%d %H:%M:%S')
                    request.session.set_expiry(300)
                    return HttpResponseRedirect(reverse('myappF23:index'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()

    return render(request, 'myappF23/login.html', {'form': form})

@login_required
def user_logout(request):
    request.session.flush()
    # logout(request)
    return HttpResponseRedirect(reverse(('myappF23:login')))


def index(request):
    cookie=0
    if 'user_visits' in request.COOKIES:
        cookie = request.COOKIES.get('user_visits', 0)
        cookie = int(cookie) + 1
    last_login_info = request.session.get('last_login_info')
    if last_login_info:
        message = f'Your last login was at: {last_login_info}'
    else:
        message = 'Your last login was more than 5 minutes ago'
    category_list = Category.objects.all().order_by('id')[:10]
    instructor_list = Instructor.objects.all().order_by('id')[:10]
    response = render(request, 'myappF23/index.html', {'category_list': category_list,'instructor_list':instructor_list,'cookie_count':cookie,'message':message})
    response.set_cookie('user_visits', cookie, max_age=10)
    return response


def about(request):
    response = HttpResponse("hello")
    response.set_cookie('user_visits', 0)
    return render(request,'myappF23/about.html')


class TestView(DetailView):
    model=Category
    template_name="myappF23/test.html"
    context_object_name = 'category'

def detail(request,category_no):
    category = get_object_or_404(Category,pk=category_no)

    courses=category.course_set.all()
    return render(request,'myappF23/detail.html',{"category":str(category),"courses":courses})

def instructor_detail(request,instructor_id):
    instructor = get_object_or_404(Instructor,pk=instructor_id)

    courses=instructor.course_set.all()

    students=instructor.students.all()

    return render(request,'myappF23/instructor_detail.html', {
        "instructor":instructor,
        "courses":courses,
        "students":students
    })

def courses(request):
    courses=Course.objects.all().order_by('id')
    return render(request,'myappF23/courses.html', {
    "courses":courses, })

def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if order.levels > order.course.levels:
                msg = 'You exceeded the number of levels for this course.'
                return render(request, 'myappF23/order_response.html', {'msg': msg})
            order.order_price = order.course.price
            if order.course.price > 150.00:
                order.discount()
            order.order_status = 0
            order.save()
            msg = 'Your course has been ordered successfully.'
        else:
            msg = 'You exceeded the number of levels for this course.'
        return render(request, 'myappF23/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myappF23/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})

def coursedetail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = InterestForm()
    if request.method=='POST':
        form=InterestForm(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']
            level = form.cleaned_data['level']
            additional_comments = form.cleaned_data['additional_comments']
            if interested == '1':
                course.interested += 1
                course.save()
            return redirect('myappF23:courses')
    return render(request,'myappF23/coursedetail.html',{'course':course,'form':form})

@login_required
def myaccount(request):
    user = request.user
    if hasattr(user, 'student'):
        student = user
        courses_ordered = Order.objects.filter(student=student)
        courses_interested = Course.objects.filter(students=student)
        context = {
            'full_name': f"{student.first_name} {student.last_name}",
            'courses_ordered': courses_ordered,
            'courses_interested': courses_interested,
            'is_student': True,
        }

        return render(request, 'myappF23/myaccount.html', context)
    else:
        return HttpResponse('You are not a registered student!')

def set_test_cookie(request):
    response = HttpResponse("Setting a test cookie")
    response.set_cookie('test_cookie', 'test_value')
    return response

def check_test_cookie(request):
    if 'test_cookie' in request.COOKIES:
        return HttpResponse("Test cookie is set! <a href='/myappF23/delete_cookie/'>Delete Cookie</a>")
    else:
        return HttpResponse("Test cookie is not set.")

def delete_test_cookie(request):
    response = HttpResponse("Deleting the test cookie")
    response.delete_cookie('test_cookie')
    return response
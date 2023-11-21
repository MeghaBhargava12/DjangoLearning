from django.urls import path
from myappF23 import views

app_name = 'myappF23'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'courses/', views.courses, name='courses'),
    path(r'test/<int:pk>', views.TestView.as_view(), name='test-detail'),
    path(r'<int:category_no>/', views.detail, name='detail'),
    path(r'instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
    path(r'place-order', views.place_order, name='place_order'),
    path(r'courses/<course_id>',views.coursedetail,name="courses_detail"),
    path(r'login/',views.user_login,name='login'),
    path(r'logout/',views.user_logout,name='logout'),
    path(r'myaccount/',views.myaccount,name='myaccount'),
    path(r'set_cookie/', views.set_test_cookie, name='set_test_cookie'),
    path(r'check_cookie/', views.check_test_cookie, name='check_test_cookie'),
    path(r'delete_cookie/', views.delete_test_cookie, name='delete_test_cookie'),
]

from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

class Student(User):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'),
        ('SP', 'Suspended'),
        ('GD', 'Graduated'), ]
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100,unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='ER')
    # courses_interested = models.ManyToManyField('Course', related_name='interested_students', blank=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    def __str__(self):
        return self.first_name + " "+self.last_name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    students= models.ManyToManyField(Student)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    COURSE_LEVEL_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'), ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    levels = models.PositiveIntegerField(choices=COURSE_LEVEL_CHOICES,default=1)
    interested= models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Order Confirmed'),
        (1, 'Order Cancelled'),
        ]
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    order_date=models.DateField()
    order_status = models.IntegerField( choices=ORDER_STATUS_CHOICES, default=1)
    order_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    levels=models.PositiveIntegerField(default=1)

    def clean(self):
        if self.levels > self.course.levels:
            raise ValidationError(_('Invalid number of levels for this course.'))
    def discount(self):
        self.order_price= self.course.price-(self.course.price*Decimal(0.1))
        self.save()

    def __str__(self):
        return f"{self.course} - {self.student} ${self.order_price}"
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from datetime import timedelta


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Person(models.Model):
    """Person abstract model"""
    GENDER_CHOICES = (
        ('m', 'Male'), ('f', 'Female')
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(
        max_length=32, blank=True, default=''
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    religion = models.CharField(
        max_length=32, blank=True, default=''
    )
    nationality = models.CharField(max_length=128)
    national_id = models.CharField(
        max_length=32, blank=True, default=''
    )
    social_security_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    health_insurance_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    
    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """"Manage for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        """Create and return a new admin user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_teacheruser(self, email, password):
        """Create and return a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_studentuser(self, email, password):
        """Create and return a new student user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_guardianuser(self, email, password):
        """Create and return a new guardian user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        related_name='users', null=True, blank=True
    )
    email = models.EmailField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class PIN(models.Model):
    PIN_TYPE_CHOICES = ( ('teacher', 'Teacher'), ('student', 'Student'), )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        blank=True, null=True, related_name='pins'
    )
    pin_code = models.CharField(max_length=10, unique=True)
    pin_type = models.CharField(max_length=7, choices=PIN_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True,
        blank=True, related_name='used_pins'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Pin {self.pin_code} ({'Used' if self.is_used else 'Available'})'

    def has_expired(self):
        if self.expire:
            return timezone.now() > self.expire
        return False

    def save(self, *args, **kwargs):
        if not self.expire:
            self.expire = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)


class Teacher(Person):
    school = models.ForeignKey(
        School, related_name='teachers', on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        related_name='teacher', blank=True, null=True
    )


class Student(Person):
    school = models.ForeignKey(
        School, related_name='students', on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        related_name='student', blank=True, null=True
    )
    grade_level = models.CharField(max_length=10)  # Example: '1st Grade', '2nd Grade'


class Subject(models.Model):
    """Subjects in the system"""
    SUBJECT_TYPES = (('core', 'Core'), ('elective', 'Elective'))
    name = models.CharField(
        max_length=255, unique=True
    )
    subject_type = models.CharField(max_length=32, choices=SUBJECT_TYPES)
    subect_code = models.CharField(
        max_length=64, unique=True, blank=True, default=''
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Lesson(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        related_name='lessons'
    )
    # e.g., algebra
    description = models.CharField(max_length=50)
    # e.g., "Fall", "Spring"
    term = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.subject.name} - ({self.term} {self.year})'


class AssignmentType(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='assignment_type',
        on_delete=models.CASCADE
    )
    # e.g., "Tests", "Quizzes"
    name = models.CharField(max_length=100)
    # Must sum to 100% across categories in a course
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Assignment(models.Model):
    assignment_type = models.ForeignKey(
        AssignmentType, related_name='assignments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    max_points = models.IntegerField()  # The maximum possible

    def __str__(self):
        return f"{self.name} ({self.assignment_type.name})"


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, related_name='enrollments',
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson, related_name='enrollments',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} enrolled in {self.lesson.name}"


class Score(models.Model):
    student = models.ForeignKey(
        Student, related_name='scores', on_delete=models.CASCADE
    )
    assignment = models.ForeignKey(
        Assignment, related_name='scores', on_delete=models.CASCADE
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'assignment')

    def __str__(self):
        return f"{self.student} - {self.assignment.name}: {self.points}/{self.assignment.max_points}"

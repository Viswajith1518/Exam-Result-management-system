from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    def is_admin_user(self):
        return self.role == 'admin'

    def is_student_user(self):
        return self.role == 'student'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    register_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    batch_year = models.IntegerField(default=2024)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.register_number} - {self.full_name}"

    def get_current_results(self):
        """Returns results for this student's current semester."""
        return self.result_set.filter(semester=self.semester)

    def calculate_gpa(self):
        """Calculate GPA from all results."""
        results = self.result_set.all()
        if not results.exists():
            return 0.0
        total_credits = sum(r.subject.credits for r in results)
        if total_credits == 0:
            return 0.0
        weighted_sum = sum(r.grade_point * r.subject.credits for r in results)
        return round(weighted_sum / total_credits, 2)


class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    credits = models.PositiveIntegerField(default=3)
    semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])

    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits} credits)"


class Result(models.Model):
    GRADE_CHOICES = (
        ('O', 'Outstanding (91-100)'),
        ('A+', 'Excellent (81-90)'),
        ('A', 'Very Good (71-80)'),
        ('B+', 'Good (61-70)'),
        ('B', 'Above Average (51-60)'),
        ('C', 'Average (40-50)'),
        ('U', 'Fail (Below 40)'),
        ('AB', 'Absent'),
    )

    GRADE_POINTS = {
        'O': 10.0,
        'A+': 9.0,
        'A': 8.0,
        'B+': 7.0,
        'B': 6.0,
        'C': 5.0,
        'U': 0.0,
        'AB': 0.0,
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(default=1)
    internal_marks = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(25)]
    )
    external_marks = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(75)]
    )
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    grade_point = models.FloatField(default=0)
    is_pass = models.BooleanField(default=False)
    exam_year = models.IntegerField(default=2024)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester', 'exam_year')

    def total_marks(self):
        return self.internal_marks + self.external_marks

    def save(self, *args, **kwargs):
        """Auto-calculate grade, grade point, and pass/fail on save."""
        total = self.total_marks()
        if self.grade == 'AB':
            self.grade_point = 0.0
            self.is_pass = False
        elif total >= 91:
            self.grade = 'O'
            self.grade_point = 10.0
            self.is_pass = True
        elif total >= 81:
            self.grade = 'A+'
            self.grade_point = 9.0
            self.is_pass = True
        elif total >= 71:
            self.grade = 'A'
            self.grade_point = 8.0
            self.is_pass = True
        elif total >= 61:
            self.grade = 'B+'
            self.grade_point = 7.0
            self.is_pass = True
        elif total >= 51:
            self.grade = 'B'
            self.grade_point = 6.0
            self.is_pass = True
        elif total >= 40:
            self.grade = 'C'
            self.grade_point = 5.0
            self.is_pass = True
        else:
            self.grade = 'U'
            self.grade_point = 0.0
            self.is_pass = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.register_number} | {self.subject.code} | {self.grade}"
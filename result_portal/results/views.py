from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser, Student, Subject, Result, Department
from .forms import StudentForm, ResultForm, StudentUserForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        login_type = request.POST.get('login_type', 'admin')

        if login_type == 'admin':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user and user.role == 'admin':
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials.')

        elif login_type == 'student':
            register_number = request.POST.get('register_number', '').strip()
            password = request.POST.get('password', '')
            try:
                student = Student.objects.get(register_number=register_number)
                user = authenticate(request, username=student.user.username, password=password)
                if user and user.role == 'student':
                    login(request, user)
                    messages.success(request, f'Welcome, {student.full_name}!')
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Incorrect password.')
            except Student.DoesNotExist:
                messages.error(request, 'Register number not found.')

    return render(request, 'results/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_results = Result.objects.count()
    recent_students = Student.objects.order_by('-created_at')[:5]
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_results': total_results,
        'recent_students': recent_students,
    }
    return render(request, 'results/admin_dashboard.html', context)


@login_required
def student_list(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    query = request.GET.get('q', '')
    students = Student.objects.select_related('department', 'user').all()
    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(register_number__icontains=query)
        )
    return render(request, 'results/student_list.html', {
        'students': students, 'query': query
    })


@login_required
def add_student(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    if request.method == 'POST':
        user_form = StudentUserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.username = student_form.cleaned_data['register_number']
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, f'Student {student.full_name} added!')
            return redirect('student_list')
    else:
        user_form = StudentUserForm()
        student_form = StudentForm()
    return render(request, 'results/add_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })


@login_required
def edit_student(request, pk):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'results/edit_student.html', {
        'form': form, 'student': student
    })


@login_required
def manage_results(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    students = Student.objects.all()
    selected_student = None
    results = []
    gpa = 0
    student_id = request.GET.get('student_id')
    if student_id:
        selected_student = get_object_or_404(Student, pk=student_id)
        results = Result.objects.filter(
            student=selected_student
        ).select_related('subject')
        gpa = selected_student.calculate_gpa()
    return render(request, 'results/manage_results.html', {
        'students': students,
        'selected_student': selected_student,
        'results': results,
        'gpa': gpa,
    })


@login_required
def add_result(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            semester = form.cleaned_data['semester']
            exam_year = form.cleaned_data['exam_year']
            result, created = Result.objects.get_or_create(
                student=student,
                subject=subject,
                semester=semester,
                exam_year=exam_year,
                defaults={
                    'internal_marks': form.cleaned_data['internal_marks'],
                    'external_marks': form.cleaned_data['external_marks'],
                }
            )
            if not created:
                result.internal_marks = form.cleaned_data['internal_marks']
                result.external_marks = form.cleaned_data['external_marks']
                result.save()
                messages.success(request, 'Result updated!')
            else:
                messages.success(request, 'Result added!')
            return redirect('manage_results')
    else:
        form = ResultForm()
    return render(request, 'results/add_result.html', {'form': form})


@login_required
def delete_result(request, pk):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    result = get_object_or_404(Result, pk=pk)
    result.delete()
    messages.success(request, 'Result deleted.')
    return redirect('manage_results')


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')
    student = get_object_or_404(Student, user=request.user)
    semester = request.GET.get('semester', student.semester)
    try:
        semester = int(semester)
    except ValueError:
        semester = student.semester
    results = Result.objects.filter(
        student=student, semester=semester
    ).select_related('subject').order_by('subject__code')
    total_subjects = results.count()
    passed = results.filter(is_pass=True).count()
    failed = results.filter(is_pass=False).count()
    gpa = student.calculate_gpa()
    total_credits = sum(r.subject.credits for r in results)
    available_semesters = Result.objects.filter(
        student=student
    ).values_list('semester', flat=True).distinct().order_by('semester')
    context = {
        'student': student,
        'results': results,
        'semester': semester,
        'gpa': gpa,
        'total_subjects': total_subjects,
        'passed': passed,
        'failed': failed,
        'total_credits': total_credits,
        'available_semesters': available_semesters,
    }
    return render(request, 'results/student_dashboard.html', context)
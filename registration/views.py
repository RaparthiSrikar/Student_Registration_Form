from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentRegistrationForm
from .models import Student, Course


from django.db.models import Count


def register(request):
    """Module 11: Handles GET (empty form) and POST (validate & save)."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student '{student.name}' registered successfully! Total registered students updated.")
            return redirect('registration:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'registration/register.html', {'form': form, 'title': 'Register as a new student', 'btn_text': 'Submit registration'})


def dashboard(request):
    """Primary home dashboard showing total registered students count, statistics, and student records."""
    students = Student.objects.prefetch_related('courses').all()
    total_students = students.count()
    male_count = students.filter(gender='M').count()
    female_count = students.filter(gender='F').count()
    other_count = students.filter(gender='O').count()
    course_stats = Course.objects.annotate(student_count=Count('students')).filter(student_count__gt=0)

    context = {
        'students': students,
        'total_students': total_students,
        'male_count': male_count,
        'female_count': female_count,
        'other_count': other_count,
        'course_stats': course_stats,
    }
    return render(request, 'registration/student_list.html', context)


def success(request):
    """Dashboard view after successful registration showing total registered students & statistics."""
    return dashboard(request)


def student_list(request):
    """Module 19: Display registered students with dashboard summary cards."""
    return dashboard(request)




def student_detail(request, pk):
    """Module 19/10: View student details."""
    student = get_object_or_404(Student.objects.prefetch_related('courses'), pk=pk)
    return render(request, 'registration/student_detail.html', {'student': student})


def student_edit(request, pk):
    """Module 10/19: Update student record."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student '{student.name}' updated successfully!")
            return redirect('registration:student_detail', pk=student.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm(instance=student)

    return render(request, 'registration/register.html', {
        'form': form,
        'student': student,
        'title': f'Edit Student: {student.name}',
        'btn_text': 'Update Student'
    })


def student_delete(request, pk):
    """Module 10/19: Delete student record."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f"Student '{name}' has been deleted successfully.")
        return redirect('registration:student_list')
    return render(request, 'registration/student_confirm_delete.html', {'student': student})


from django.contrib import admin
from .models import Student, Course

admin.site.register(Course)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'phone_number', 'email', 'gender', 'display_courses', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('gender', 'courses')

    def display_courses(self, obj):
        return ", ".join([c.name for c in obj.courses.all()])
    display_courses.short_description = 'Courses'


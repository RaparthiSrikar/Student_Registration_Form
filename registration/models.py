from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Course(models.Model):
    """Module 15: Course entity - separate table for clean DB design."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """Module 8: Student model - stores registration data with DB-level validation."""

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    phone_number = models.CharField(
        max_length=10, unique=True, validators=[phone_regex]
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    courses = models.ManyToManyField(
        Course, related_name='students'
    )
    profile_image = models.ImageField(upload_to='student_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ['-created_at']

from django import forms
from django.core.validators import FileExtensionValidator
from .models import Student, Course


class StudentRegistrationForm(forms.ModelForm):
    """Module 12: Server-side validation for every field."""

    name = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age',
            'min': '1',
            'max': '120',
            'onkeydown': 'return event.key >= "0" && event.key <= "9" || ["Backspace","Tab","ArrowLeft","ArrowRight","Delete","Enter"].includes(event.key)',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '10-digit phone number',
            'maxlength': '10',
            'onkeydown': 'return event.key >= "0" && event.key <= "9" || ["Backspace","Tab","ArrowLeft","ArrowRight","Delete","Enter"].includes(event.key)',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 10)'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
            'onkeydown': 'return event.key !== " "',
            'oninput': 'this.value = this.value.replace(/\\s/g, "").toLowerCase()'
        })
    )
    gender = forms.ChoiceField(
        choices=Student.GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    profile_image = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Student
        fields = ['name', 'age', 'phone_number', 'email', 'gender', 'courses', 'profile_image']

    # --- Module 21 test cases enforced below ---

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        if not all(c.isalpha() or c.isspace() for c in name):
            raise forms.ValidationError("Name should contain only letters and spaces.")
        if len(name) < 2:
            raise forms.ValidationError("Name is too short.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            raise forms.ValidationError("Age is required.")
        if age <= 0:
            raise forms.ValidationError("Age must be positive.")
        return age

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        qs = Student.objects.filter(phone_number=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        qs = Student.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_courses(self):
        courses = self.cleaned_data.get('courses')
        if not courses or len(courses) == 0:
            raise forms.ValidationError("Select at least one course.")
        return courses

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if not self.instance.pk and not image:
            raise forms.ValidationError("Profile image is required.")
        if image and hasattr(image, 'size'):
            max_size_mb = 2
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(f"Image size must be under {max_size_mb}MB.")
        return image


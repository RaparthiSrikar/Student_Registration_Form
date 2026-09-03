from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Student, Course
from .forms import StudentRegistrationForm


class StudentFormAndModelTestCase(TestCase):
    """Module 21: Unit tests for client & server validation and CRUD views."""

    def setUp(self):
        self.course1 = Course.objects.create(name="Python Full Stack")
        self.course2 = Course.objects.create(name="Django")

        # Existing student for duplicate phone & email tests
        self.existing_student = Student.objects.create(
            name="Alice Smith",
            age=22,
            phone_number="9876543210",
            email="alice@example.com",
            gender="F",
            profile_image=self.get_test_image()
        )
        self.existing_student.courses.add(self.course1)

    def get_test_image(self, name='test_avatar.png'):
        return SimpleUploadedFile(
            name=name,
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/png'
        )

    def valid_data(self, **kwargs):
        data = {
            'name': 'John Doe',
            'age': 25,
            'phone_number': '1122334455',
            'email': 'john@example.com',
            'gender': 'M',
            'courses': [self.course1.id]
        }
        data.update(kwargs)
        return data

    def validate(self, data, image=None):
        img = image if image is not None else self.get_test_image()
        return StudentRegistrationForm(data=data, files={'profile_image': img})

    def test_name_validation(self):
        # Test empty, non-alphabetic, too short vs valid
        for invalid_name in ['', 'John123', 'J']:
            self.assertFalse(self.validate(self.valid_data(name=invalid_name)).is_valid())
        self.assertTrue(self.validate(self.valid_data(name='John Doe')).is_valid())

    def test_age_validation(self):
        # Test zero, negative, non-numeric, special characters vs valid positive integer
        for invalid_age in [0, -5, 'abc', '25@#']:
            self.assertFalse(self.validate(self.valid_data(age=invalid_age)).is_valid())
        self.assertTrue(self.validate(self.valid_data(age=25)).is_valid())

    def test_phone_validation(self):
        # Test empty, short, alphabetic, special chars, and duplicate phone vs valid 10-digit number
        for invalid_phone in ['', '12345', '12345abcde', '98765-4321', '9876543210']:
            self.assertFalse(self.validate(self.valid_data(phone_number=invalid_phone)).is_valid())
        self.assertTrue(self.validate(self.valid_data(phone_number='1122334455')).is_valid())

    def test_email_validation(self):
        # Test empty, missing domain, missing @, and duplicate email vs valid format
        for invalid_email in ['', 'invalid-email', 'test.domain.com', 'alice@example.com']:
            self.assertFalse(self.validate(self.valid_data(email=invalid_email)).is_valid())
        self.assertTrue(self.validate(self.valid_data(email='new@example.com')).is_valid())

    def test_gender_validation(self):
        self.assertFalse(self.validate(self.valid_data(gender='')).is_valid())
        self.assertTrue(self.validate(self.valid_data(gender='M')).is_valid())

    def test_course_validation(self):
        self.assertFalse(self.validate(self.valid_data(courses=[])).is_valid())
        self.assertTrue(self.validate(self.valid_data(courses=[self.course1.id, self.course2.id])).is_valid())

    def test_image_validation(self):
        txt_file = SimpleUploadedFile("test.txt", b"txt", content_type="text/plain")
        large_file = SimpleUploadedFile("large.png", b"0" * (3 * 1024 * 1024), content_type="image/png")
        self.assertFalse(self.validate(self.valid_data(), image=txt_file).is_valid())
        self.assertFalse(self.validate(self.valid_data(), image=large_file).is_valid())

    def test_views_and_crud(self):
        client = Client()
        for url_name in ['registration:dashboard', 'registration:register', 'registration:student_list']:
            self.assertEqual(client.get(reverse(url_name)).status_code, 200)

        detail_url = reverse('registration:student_detail', kwargs={'pk': self.existing_student.pk})
        self.assertContains(client.get(detail_url), "Alice Smith")

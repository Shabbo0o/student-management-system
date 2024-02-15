from django.test import TestCase
from django.urls import reverse
from .models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        # Create a sample student for testing
        self.student_data = {
            'student_number': 12345,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'field_of_study': 'Computer Science',
            'gpa': 3.8,
        }
        self.student = Student.objects.create(**self.student_data)

    def test_add_student_view(self):
        # Test that the add student view returns a successful response
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)

    def test_add_student_form_submission(self):
        # Test that submitting the form adds a new student
        new_student_data = {
            'student_number': 54321,
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'field_of_study': 'Physics',
            'gpa': 3.5,
        }

        response = self.client.post(reverse('add'), data=new_student_data)

        # Check that the student was added to the database
        self.assertEqual(Student.objects.count(), 2)

        # Check that the response is a redirect (successful form submission)
        self.assertEqual(response.status_code, 302)

        # Optionally, you can check that the newly added student is in the database
        new_student = Student.objects.get(
            student_number=new_student_data['student_number'])
        self.assertEqual(new_student.first_name, 'Jane')
        self.assertEqual(new_student.last_name, 'Smith')
        # Add more assertions as needed

    def test_add_student_form_invalid_submission(self):
        # Test that submitting an invalid form does not add a new student
        invalid_student_data = {
            'student_number': 'invalid',  # Invalid data, student_number should be a number
            'first_name': 'Invalid',
            'last_name': 'Student',
            'email': 'invalid.student@example.com',
            'field_of_study': 'Invalid Field',
            'gpa': 'invalid',  # Invalid data, GPA should be a number
        }

        response = self.client.post(reverse('add'), data=invalid_student_data)

        # Check that the student was not added to the database
        self.assertEqual(Student.objects.count(), 1)

        # Check that the response is not a redirect (form submission failed)
        self.assertEqual(response.status_code, 200)

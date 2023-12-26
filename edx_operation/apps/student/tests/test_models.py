from django.core.exceptions import ValidationError
from django.test import TestCase

from edx_operation.apps.student.models import Student
from edx_operation.apps.core.utils.common import encrypt_id_number


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            id="sample_id",
            email="sample_email@example.com",
        )

    def test_set_id_number_valid(self):
        valid_id_number = "200101-1234123"
        self.student.set_id_number(valid_id_number)

        # Ensure id_number is encrypted correctly
        self.assertEqual(self.student.id_number, encrypt_id_number(valid_id_number))

    def test_set_id_number_invalid_format(self):
        # Test with an invalid id_number format
        invalid_id_number = "2010101234123"

        # Ensure a ValidationError is raised
        with self.assertRaises(ValidationError):
            self.student.set_id_number(invalid_id_number)

        # Ensure id_number remains unchanged
        self.assertIsNone(self.student.id_number)

    def test_check_id_number_matching(self):
        # Set a valid id_number
        valid_id_number = "200101-1234123"
        self.student.set_id_number(valid_id_number)

        # Test with a matching id_number
        self.assertTrue(self.student.check_id_number(valid_id_number))

    def test_check_id_number_non_matching(self):
        # Set a valid id_number
        valid_id_number = "200101-1234123"
        self.student.set_id_number(valid_id_number)

        # Test with a non-matching id_number
        non_matching_id_number = "741002-1234567"
        self.assertFalse(self.student.check_id_number(non_matching_id_number))

import os
from datetime import date
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import AdmissionStudent
from academics.models import Department


class TestStudentsViews(TestCase):

    def create_department(self):
        cmt = Department.objects.create(
            name='Computer',
            short_name='cmt',
            code=121,
        )
        return cmt

    def create_paid_admitted_registrant(self):
        img_path = os.path.join(
            settings.MEDIA_ROOT,
            AdmissionStudent.photo.field.upload_to,
            'test_image.png'
        )
        dept = self.create_department()
        student = AdmissionStudent.objects.create(
            name='TestStudent',
            photo=SimpleUploadedFile(
                name='test_image.png', 
                content=open(img_path, 'rb').read(), 
                content_type='image/jpeg'
            ),
            fathers_name='testfather',
            mothers_name='testmother',
            date_of_birth=date.today(),
            email='tareqmonwer137@gmail.com',
            city='13',
            current_address='testaddress',
            permanent_address='testparmanentaddress',
            mobile_number='12121212',
            guardian_mobile_number='2233223',
            tribal_status=0,
            children_of_freedom_fighter=0,
            department_choice=dept,
            choosen_department=dept,
            exam_name='HSC',
            passing_year='2020',
            group='general',
            board='dhaka',
            ssc_roll='12121',
            ssc_registration='121212121',
            gpa=2.00,
            admitted=True,
            paid=True
        )
        return student

    def test_create_paid_admitted_registrant(self):
        student = self.create_paid_admitted_registrant()
        self.assertTrue(isinstance(student, AdmissionStudent))
        self.assertTrue(student.email, 'tareqmonwer137@gmail.com')

    def test_admit_student_view_get(self):
        student = self.create_paid_admitted_registrant()
        response = self.client.get(reverse(
            'students:admit_student', args=[student.id, ]
        ))
        self.assertTrue(response.status_code, 200)
    
    def test_admit_student_view_post(self):
        student = self.create_paid_admitted_registrant()
        response = self.client.post(
            reverse('students:admit_student', args=[student.id, ])
        )
        self.assertTrue(response.status_code, 201)
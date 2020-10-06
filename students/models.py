from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from academics.models import Department, Semester, AcademicSession


class StudentBase(TimeStampedModel):
    LAST_EXAMS = (
        ('HSC', 'Higher Secondary Certificate'),
        ('SSC', 'Secondary School Certificate'),
        ('DAKHIL', 'Dakhil Exam'),
        ('JDC', 'Junior Dakhil Certificate'),
    )
    name = models.CharField("Full Name", max_length=100)
    photo = models.ImageField(upload_to='students/applicant/')
    fathers_name = models.CharField("Father's Name", max_length=100)
    mothers_name = models.CharField("Mother's Name", max_length=100)
    date_of_birth = models.DateField("Birth Date", blank=True, null=True)
    email = models.EmailField("Email Address")
    current_address = models.TextField()
    permanent_address = models.TextField()
    mobile_number = models.CharField('Mobile Number', max_length=11)
    department_choice = models.ForeignKey(Department, 
        on_delete=models.CASCADE)
    last_exam_name = models.CharField(
        'Last Exam', choices=LAST_EXAMS, max_length=2)
    last_exam_roll = models.CharField(max_length=10)
    last_exam_registration = models.CharField(max_length=10)
    last_exam_result = models.CharField(max_length=5)


    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


class AdmissionStudent(StudentBase):
    pass


class Student(StudentBase):
    roll = models.CharField(max_length=6, unique=True)
    registration_number = models.CharField(max_length=6, unique=True)
    department = models.ForeignKey(Department, 
        on_delete=models.CASCADE, related_name='departments')
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE)
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=11, blank=True, null=True)
    admitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)
    is_alumni = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False)

    def has_subjects(self):
        from result.models import SubjectCombination
        return SubjectCombination.objects.filter(
            semester=self.semester, department=self.department
        )

    def __str__(self):
        return '{} ({}) semester {} dept.'.format(
            self.name, self.semester, self.department
        )

    class Meta:
        ordering = ['semester', 'roll', 'registration_number']

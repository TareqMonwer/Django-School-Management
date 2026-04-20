from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_school_management.academics.models import Department, Batch, AcademicSession
from ..models import Student, AdmissionStudent

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='head.name', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'short_name', 'code', 'short_description',
            'department_icon', 'head', 'head_name', 'current_batch',
            'establish_date', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']


class BatchSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    academic_session = serializers.CharField(source='year.__str__', read_only=True)
    
    class Meta:
        model = Batch
        fields = [
            'id', 'year', 'number', 'department', 'department_name',
            'academic_session', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']


class AdmissionStudentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department_choice.name', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = AdmissionStudent
        fields = [
            'id', 'name', 'photo', 'fathers_name', 'mothers_name',
            'date_of_birth', 'age', 'email', 'mobile_number',
            'department_choice', 'department_name', 'exam_name',
            'passing_year', 'gpa', 'admitted', 'paid', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']
    
    def get_age(self, obj):
        from datetime import date
        if obj.date_of_birth:
            today = date.today()
            return today.year - obj.date_of_birth.year - (
                (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        return None


class StudentSerializer(serializers.ModelSerializer):
    """Serialize Student; exposes related admission_student and batch/department via source."""
    department = serializers.SerializerMethodField()
    batch = BatchSerializer(read_only=True)
    admission_student = AdmissionStudentSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    academic_status = serializers.SerializerMethodField()
    name = serializers.CharField(source='admission_student.name', read_only=True)
    photo = serializers.ImageField(source='admission_student.photo', read_only=True)
    fathers_name = serializers.CharField(source='admission_student.fathers_name', read_only=True)
    mothers_name = serializers.CharField(source='admission_student.mothers_name', read_only=True)
    date_of_birth = serializers.DateField(source='admission_student.date_of_birth', read_only=True)
    email = serializers.EmailField(source='admission_student.email', read_only=True)
    mobile_number = serializers.CharField(source='admission_student.mobile_number', read_only=True)
    roll_number = serializers.CharField(source='roll', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'admission_student', 'name', 'photo',
            'fathers_name', 'mothers_name', 'date_of_birth', 'email',
            'mobile_number', 'department', 'batch', 'roll_number',
            'registration_number', 'full_name', 'academic_status',
            'is_alumni', 'is_dropped', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']

    def get_department(self, obj):
        if obj.batch and obj.batch.department_id:
            return DepartmentSerializer(obj.batch.department).data
        return None

    def get_full_name(self, obj):
        return obj.admission_student.name if obj.admission_student_id else None

    def get_academic_status(self, obj):
        if obj.is_alumni:
            return "Alumni"
        elif obj.is_dropped:
            return "Dropped"
        return "Active"


class StudentCreateSerializer(serializers.ModelSerializer):
    """Create a Student from an existing AdmissionStudent and batch/semester/session."""

    class Meta:
        model = Student
        fields = [
            'admission_student', 'batch', 'semester', 'ac_session',
            'roll', 'registration_number', 'guardian_mobile'
        ]

    def create(self, validated_data):
        return Student.objects.create(**validated_data)


class StudentBulkActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['activate', 'deactivate', 'delete', 'assign_batch'])
    student_ids = serializers.ListField(child=serializers.IntegerField())
    batch_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate(self, attrs):
        if attrs['action'] == 'assign_batch' and not attrs.get('batch_id'):
            raise serializers.ValidationError("Batch ID is required for assign_batch action.")
        return attrs

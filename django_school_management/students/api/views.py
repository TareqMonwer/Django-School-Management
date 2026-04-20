from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone

from ..models import Student, AdmissionStudent
from .filters import StudentFilterSet
from .serializers import (
    StudentSerializer, StudentCreateSerializer, 
    AdmissionStudentSerializer, StudentBulkActionSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing students.
    
    Provides:
    - CRUD operations for students
    - Advanced filtering and search
    - Bulk operations
    - Analytics endpoints
    """
    queryset = Student.objects.all().select_related(
        'batch', 'batch__department', 'admission_student'
    )
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = StudentFilterSet
    search_fields = [
        'admission_student__name', 'admission_student__email',
        'roll', 'registration_number'
    ]
    ordering_fields = ['created', 'roll', 'registration_number']
    ordering = ['-created']

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_action']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by academic status
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_alumni=False, is_dropped=False)
        elif status_filter == 'alumni':
            queryset = queryset.filter(is_alumni=True)
        elif status_filter == 'dropped':
            queryset = queryset.filter(is_dropped=True)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created__gte=start_date)
        if end_date:
            queryset = queryset.filter(created__lte=end_date)
        
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """
        Perform bulk actions on students:
        - activate: Mark students as active
        - deactivate: Mark students as dropped
        - delete: Soft delete students
        - assign_batch: Assign students to a batch
        """
        serializer = StudentBulkActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action = serializer.validated_data['action']
        student_ids = serializer.validated_data['student_ids']
        batch_id = serializer.validated_data.get('batch_id')
        
        students = Student.objects.filter(id__in=student_ids)
        count = students.count()
        
        if action == 'activate':
            students.update(is_alumni=False, is_dropped=False)
            message = f"Activated {count} students"
        elif action == 'deactivate':
            students.update(is_dropped=True)
            message = f"Deactivated {count} students"
        elif action == 'delete':
            students.update(is_dropped=True)
            message = f"Soft deleted {count} students"
        elif action == 'assign_batch':
            from django_school_management.academics.models import Batch
            batch = Batch.objects.get(id=batch_id)
            students.update(batch=batch)
            message = f"Assigned {count} students to batch {batch}"
        
        return Response({
            'message': message,
            'affected_count': count
        })

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get student analytics:
        - Total students by status
        - Students by department
        - Admission trends
        - Demographics
        """
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        # Basic counts
        total_students = Student.objects.count()
        active_students = Student.objects.filter(is_alumni=False, is_dropped=False).count()
        alumni_students = Student.objects.filter(is_alumni=True).count()
        dropped_students = Student.objects.filter(is_dropped=True).count()
        
        # Students by department (via batch)
        department_stats = Student.objects.values(
            'batch__department__name'
        ).annotate(count=Count('id')).order_by('-count')

        # Admission trends (last 12 months)
        twelve_months_ago = timezone.now() - timedelta(days=365)
        from django.db.models.functions import TruncMonth
        admission_trends = Student.objects.filter(
            created__gte=twelve_months_ago
        ).annotate(
            month=TruncMonth('created')
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        # Recent admissions
        recent_admissions = AdmissionStudent.objects.filter(
            created__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        return Response({
            'overview': {
                'total_students': total_students,
                'active_students': active_students,
                'alumni_students': alumni_students,
                'dropped_students': dropped_students,
                'recent_admissions': recent_admissions
            },
            'department_distribution': list(department_stats),
            'admission_trends': list(admission_trends)
        })

    @action(detail=True, methods=['get'])
    def academic_history(self, request, pk=None):
        """
        Get academic history for a specific student
        """
        student = self.get_object()
        
        # Get academic records, results, attendance etc.
        # This would be implemented based on your actual academic models
        
        return Response({
            'student': StudentSerializer(student).data,
            'academic_records': [],  # Implement based on your models
            'results': [],  # Implement based on your result models
            'attendance': []  # Implement based on your attendance models
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Export student data in various formats (CSV, Excel)
        """
        format_type = request.query_params.get('format', 'csv')
        
        # This would implement actual export functionality
        # Using django-import-export or similar
        
        return Response({
            'message': f'Export functionality for {format_type} format',
            'download_url': '/api/students/download/export.csv'
        })


class AdmissionStudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing admission applications
    """
    queryset = AdmissionStudent.objects.all().select_related('department_choice')
    serializer_class = AdmissionStudentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department_choice', 'admitted', 'paid']
    search_fields = ['name', 'email', 'mobile_number']
    ordering_fields = ['name', 'created', 'gpa']
    ordering = ['-created']

    @action(detail=True, methods=['post'])
    def approve_admission(self, request, pk=None):
        """
        Approve admission and convert to regular student
        """
        admission_student = self.get_object()
        
        if admission_student.admitted:
            return Response({
                'error': 'Student already admitted'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Logic to convert admission student to regular student
        # This would involve creating a Student instance and User account
        
        return Response({
            'message': 'Admission approved successfully',
            'student_id': admission_student.id
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get admission statistics
        """
        from django.db.models import Count, Q
        
        total_applications = AdmissionStudent.objects.count()
        admitted_count = AdmissionStudent.objects.filter(admitted=True).count()
        paid_count = AdmissionStudent.objects.filter(paid=True).count()
        pending_count = total_applications - admitted_count
        
        # Applications by department
        dept_stats = AdmissionStudent.objects.values('department_choice__name').annotate(
            count=Count('id'),
            admitted=Count('id', filter=Q(admitted=True))
        ).order_by('-count')
        
        return Response({
            'total_applications': total_applications,
            'admitted_count': admitted_count,
            'paid_count': paid_count,
            'pending_count': pending_count,
            'conversion_rate': round((admitted_count / total_applications * 100) if total_applications > 0 else 0, 2),
            'department_stats': list(dept_stats)
        })

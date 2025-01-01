from enum import Enum


class StudentsURLEnums(Enum):
    students_dashboard_index = ""
    test_pdf = "pdf/"
    add_student = "add/"
    all_student = "all/"
    alumnus = "alumnus/"
    all_applicants = "applicants/"
    unpaid_registrants = "applicants/unpaid/"
    mark_as_paid_or_unpaid = "applicants/mark-paid/"
    add_counseling_data = "add-counsel-data/<int:student_id>/"
    admitted_student_list = "admitted-students/"
    admission_confirmation = "admission-confirm/"
    get_json_batch_data = "api/batches/<int:department_code>/"
    yearly_graph_api = "api/yearly-graph/"
    admit_student = "online-applicants/<int:pk>/admit/"
    paid_registrants = "paid-registrants/"
    rejected_registrants = "rejected-registrants/"
    update_online_registrant = "update-registrant/<int:pk>/"
    update_student = "update/<int:pk>/"
    student_details = "<int:pk>/detail/"
    delete_student = "<int:pk>/delete/"
    students_by_dept = "<int:pk>/students/"
    counsel_monthly_report = "counsel-report/"
    counsel_monthly_report_typed = "counsel-report/<str:response_type>/"
    counsel_report_monthly_with_date = "counsel-report/<str:response_type>/<date:date_param>/"
    student_my_portal = "my-portal/<str:student_id>"


class StudentsURLConstants:
    students_dashboard_index = f"students:{StudentsURLEnums.students_dashboard_index.name}"
    test_pdf = f"students:{StudentsURLEnums.test_pdf.name}"
    add_student = f"students:{StudentsURLEnums.add_student.name}"
    all_student = f"students:{StudentsURLEnums.all_student.name}"
    alumnus = f"students:{StudentsURLEnums.alumnus.name}"
    all_applicants = f"students:{StudentsURLEnums.all_applicants.name}"
    unpaid_registrants = f"students:{StudentsURLEnums.unpaid_registrants.name}"
    mark_as_paid_or_unpaid = f"students:{StudentsURLEnums.mark_as_paid_or_unpaid.name}"
    add_counseling_data = f"students:{StudentsURLEnums.add_counseling_data.name}"
    admitted_student_list = f"students:{StudentsURLEnums.admitted_student_list.name}"
    admission_confirmation = f"students:{StudentsURLEnums.admission_confirmation.name}"
    get_json_batch_data = f"students:{StudentsURLEnums.get_json_batch_data.name}"
    yearly_graph_api = f"students:{StudentsURLEnums.yearly_graph_api.name}"
    admit_student = f"students:{StudentsURLEnums.admit_student.name}"
    paid_registrants = f"students:{StudentsURLEnums.paid_registrants.name}"
    rejected_registrants = f"students:{StudentsURLEnums.rejected_registrants.name}"
    update_online_registrant = f"students:{StudentsURLEnums.update_online_registrant.name}"
    update_student = f"students:{StudentsURLEnums.update_student.name}"
    student_details = f"students:{StudentsURLEnums.student_details.name}"
    delete_student = f"students:{StudentsURLEnums.delete_student.name}"
    students_by_dept = f"students:{StudentsURLEnums.students_by_dept.name}"
    counsel_monthly_report = f"students:{StudentsURLEnums.counsel_monthly_report.name}"
    counsel_monthly_report_typed = f"students:{StudentsURLEnums.counsel_monthly_report_typed.name}"
    counsel_report_monthly_with_date = f"students:{StudentsURLEnums.counsel_report_monthly_with_date.name}"
    student_my_portal = f"students:{StudentsURLEnums.student_my_portal.name}"
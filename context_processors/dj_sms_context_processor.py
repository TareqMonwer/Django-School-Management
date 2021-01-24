from institute.models import InstituteProfile

def attach_institute_data_ctx_processor(request):
    institute = InstituteProfile.objects.get(active=True)
    return {'request_institute': institute, }

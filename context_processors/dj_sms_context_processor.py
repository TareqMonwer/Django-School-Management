from institute.models import InstituteProfile
from articles.models import Category

def attach_institute_data_ctx_processor(request):
    institute = InstituteProfile.objects.get(active=True)
    registered_navlinks = Category.objects.filter(
        display_on_menu=True,
    ).order_by('-created')
    return {
        'request_institute': institute,
        'registered_navlinks': registered_navlinks
    }

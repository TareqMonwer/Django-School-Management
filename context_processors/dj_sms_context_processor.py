from institute.models import InstituteProfile
from articles.models import Category

def attach_institute_data_ctx_processor(request):
    institute = InstituteProfile.objects.get(active=True)

    ctx = {
        'request_institute': institute,
    }
    if 'articles' in request.resolver_match._func_path.split('.'):
        # If request is coming for articles app's views,
        # only then pass registered_navlinks in the context.
        registered_navlinks = Category.objects.filter(
            display_on_menu=True,
        ).order_by('-created')
        ctx['registered_navlinks'] = registered_navlinks
    return ctx

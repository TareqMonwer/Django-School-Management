from institute.models import (InstituteProfile,
        TextWidget, ListWidget
)
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
        try:
            # first text-widget for the footer (footer-col-number-1)
            first_widget =  TextWidget.objects.get(widget_number=0)
            # get rest three widgets
            list_widgets = ListWidget.objects.filter(widget_number__lte=4)
        except (TextWidget.DoesNotExist, Exception):
            first_widget = None
            list_widgets = None

        ctx['registered_navlinks'] = registered_navlinks
        ctx['first_widget'] = first_widget
        ctx['list_widgets'] = list_widgets
    return ctx

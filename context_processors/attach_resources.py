from django_school_management.academics.constants import AcademicsURLConstants
from django_school_management.accounts.constants import AccountURLConstants
from django_school_management.accounts.services.menu import MenuService
from django_school_management.accounts.utils.menu_config import get_menu_config
from django_school_management.institute.models import (
    InstituteProfile,
    TextWidget,
    ListWidget,
)
from django_school_management.articles.models import Category


def attach_institute_data_ctx_processor(request):
    institute = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        institute = getattr(request.user, 'institute', None)
    if not institute:
        try:
            institute = InstituteProfile.objects.get(active=True)
        except InstituteProfile.DoesNotExist:
            institute = None
    ctx = {
        "request_institute": institute,
    }

    if "articles" in request.resolver_match._func_path.split("."):
        # If request is coming for articles app's views,
        # only then pass registered_navlinks in the context.
        # Registered navlinks are Category objects from the articles app.
        try:
            registered_navlinks = Category.objects.filter(
                display_on_menu=True,
            ).order_by("-created")
        except:
            registered_navlinks = []
        try:
            # Setting up widgets for footer and other places of the
            # website. (TODO: Add location hints to the widget models).
            # first text-widget for the footer (footer-col-number-1)
            first_widget = TextWidget.objects.get(widget_number=0)
            # get rest three widgets
            list_widgets = ListWidget.objects.filter(widget_number__lte=4)
        except (TextWidget.DoesNotExist, Exception):
            first_widget = None
            list_widgets = None

        ctx["registered_navlinks"] = registered_navlinks
        ctx["first_widget"] = first_widget
        ctx["list_widgets"] = list_widgets
    return ctx


def attach_urls_for_common_templates(request):
    return dict(
        account_urls=AccountURLConstants,
        academic_urls=AcademicsURLConstants,
    )


def attach_dashboard_menu_items(request):
    if request.user.is_authenticated:
        menu_cofig = get_menu_config(request.user)
        menu_service = MenuService(menu_cofig)
        student_menu_items = menu_service.get_menu_items(
            "student", request.user
        )
        teacher_menu_items = menu_service.get_menu_items(
            "teacher", request.user
        )
        return dict(
            student_menu_items=student_menu_items,
            teacher_menu_items=teacher_menu_items,
        )
    return dict(
        student_menu_items=[],
        teacher_menu_items=[],
    )

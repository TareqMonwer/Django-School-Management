from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # overriding app name and label to avoid conflict with 
    name = 'django_school_management.accounts'
    
    def ready(self):
        pass

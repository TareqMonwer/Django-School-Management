from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # overriding app name and label to avoid conflict with 
    name = 'accounts'
    
    def ready(self):
        import accounts.signals

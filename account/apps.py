from django.apps import AppConfig


class AccountConfig(AppConfig):
    # overriding app name and label to avoid conflict with 
    name = 'account'
    # label = 'local_account'
    # verbose_name = 'local_accounts'

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # overriding app name and label to avoid conflict with 
    name = 'accounts'
    # label = 'local_account'
    # verbose_name = 'local_accounts'

from django.apps import AppConfig
from django.db.models.signals import post_migrate,post_save

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        pass
        # from accounts.signals import create_first_account
        # post_migrate.connect(create_first_account, sender=self)

        





    
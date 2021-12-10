from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    # uncomment after migrations if want to do the checks at the end of class registration period
    # def ready(self):
    #     from .updater import start
    #     start()

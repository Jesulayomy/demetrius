from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """ Library application configuration """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

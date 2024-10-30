from django.apps import AppConfig


class MetalworksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metalworks'
    verbose_name = 'Металлобработка'

    def ready(self) -> None:
        import pressforms.signals
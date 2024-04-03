from django.apps import AppConfig

class PressformsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pressforms'
    verbose_name = 'Прессформы'

    def ready(self) -> None:
        import pressforms.signals

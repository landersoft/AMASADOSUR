from django.apps import AppConfig


class AbastecimientoConfig(AppConfig):
    name = 'abastecimiento'

    def ready(self):
        import abastecimiento.signals.handlers
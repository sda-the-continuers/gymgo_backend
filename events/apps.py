from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'

    def try_import_handlers(self, name):
        import importlib
        try:
            importlib.import_module(f'{name}.event_handlers')
        except ModuleNotFoundError:
            pass

    def ready(self):
        from django.apps import apps
        for app_config in apps.get_app_configs():
            self.try_import_handlers(name=app_config.name)
        super().ready()

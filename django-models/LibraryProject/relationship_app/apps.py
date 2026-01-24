from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    name = 'relationship_app'

    def ready(self):
        import relationship_app.models  # Ensure signals are loaded

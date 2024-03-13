from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Student'
    def ready(self):
        import Student.signals  # This will import and connect your signals when the app is ready

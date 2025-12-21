from django.apps import AppConfig


class NeurovaAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "neurova_admin"
    verbose_name = "Neurova Admin"

    def ready(self):
        # 🔥 Force admin registration
        import neurova_admin.admin  # noqa

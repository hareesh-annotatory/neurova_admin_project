from django.contrib import admin
from .models import DatasetUpload, TrainingSample, SystemEvent

class ReadOnlyAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


@admin.register(DatasetUpload)
class DatasetUploadAdmin(ReadOnlyAdmin):
    list_display = ("id", "name", "dataset_type", "format", "source", "is_processed", "created_at")
    search_fields = ("id", "name", "dataset_type", "source")
    list_filter = ("dataset_type", "source", "is_processed")
    ordering = ("-created_at",)
    list_per_page = 50


@admin.register(TrainingSample)
class TrainingSampleAdmin(ReadOnlyAdmin):
    list_display = ("id", "sample_type", "chosen_output", "is_labeled", "label", "created_at")
    search_fields = ("id", "sample_type", "label", "chosen_output")
    list_filter = ("sample_type", "chosen_output", "is_labeled", "label")
    ordering = ("-created_at",)
    list_per_page = 50


@admin.register(SystemEvent)
class SystemEventAdmin(ReadOnlyAdmin):
    list_display = ("id", "event_type", "severity", "source", "created_at")
    search_fields = ("id", "event_type", "severity", "source")
    list_filter = ("severity", "source", "event_type")
    ordering = ("-created_at",)
    list_per_page = 50

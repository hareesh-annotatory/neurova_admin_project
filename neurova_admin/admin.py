from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import (
    TrainingSample,
    DatasetUpload,
    SystemEvent,
    HumanLabel,
    PromotionRequest,
    ModelRouteLog,
)


class ReadOnlyAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TrainingSample)
class TrainingSampleAdmin(ReadOnlyAdmin):
    list_display = ("id", "sample_type", "chosen_output", "is_labeled", "created_at")
    search_fields = ("id", "sample_type")
    ordering = ("-created_at",)
    readonly_fields = [f.name for f in TrainingSample._meta.fields]


@admin.register(DatasetUpload)
class DatasetUploadAdmin(ReadOnlyAdmin):
    list_display = ("id", "name", "dataset_type", "source", "is_processed", "created_at")
    search_fields = ("id", "name")
    ordering = ("-created_at",)
    readonly_fields = [f.name for f in DatasetUpload._meta.fields]


@admin.register(SystemEvent)
class SystemEventAdmin(ReadOnlyAdmin):
    list_display = ("id", "event_type", "severity", "source", "created_at")
    search_fields = ("event_type", "source")
    ordering = ("-created_at",)
    readonly_fields = [f.name for f in SystemEvent._meta.fields]


@admin.register(ModelRouteLog)
class ModelRouteLogAdmin(ReadOnlyAdmin):
    list_display = ("id", "route_mode", "pipeline", "created_at")
    list_filter = ("route_mode", "pipeline")
    ordering = ("-created_at",)
    readonly_fields = [f.name for f in ModelRouteLog._meta.fields]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.defer("rule_output", "llm_output", "diff_summary")

@admin.register(HumanLabel)
class HumanLabelAdmin(admin.ModelAdmin):
    list_display = ("id", "sample_type", "sample_id", "review_status", "reviewer", "created_at")
    list_filter = ("sample_type", "review_status", "reviewer")
    search_fields = ("sample_id", "reviewer")
    actions = ["approve_labels", "reject_labels", "export_labels"]

    @admin.action(description="Approve selected labels")
    def approve_labels(self, request, queryset):
        queryset.update(review_status="approved")

    @admin.action(description="Reject selected labels")
    def reject_labels(self, request, queryset):
        queryset.update(review_status="rejected")

    @admin.action(description="Export selected labels as CSV")
    def export_labels(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="human_labels.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "id",
            "sample_type",
            "sample_id",
            "review_status",
            "reviewer",
            "label_json",
            "created_at",
        ])
        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.sample_type,
                obj.sample_id,
                obj.review_status,
                obj.reviewer,
                obj.label_json,
                obj.created_at,
            ])
        return response


@admin.register(PromotionRequest)
class PromotionRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "target_type", "target_version", "status", "requested_by", "created_at")
    list_filter = ("target_type", "status")
    search_fields = ("target_version", "requested_by")
    readonly_fields = ("created_at",)

    @admin.action(description="Approve promotion request")
    def approve_request(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Reject promotion request")
    def reject_request(self, request, queryset):
        queryset.update(status="rejected")

    actions = ["approve_request", "reject_request"]

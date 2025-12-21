from django.contrib import admin
from .models import TrainingSample, DatasetUpload, SystemEvent


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(TrainingSample, ReadOnlyAdmin)
admin.site.register(DatasetUpload, ReadOnlyAdmin)
admin.site.register(SystemEvent, ReadOnlyAdmin)

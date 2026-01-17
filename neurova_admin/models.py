from django.db import models


# =========================
# ENGINE TABLES (READ ONLY)
# =========================

class TrainingSample(models.Model):
    id = models.UUIDField(primary_key=True)
    patient_id = models.UUIDField(null=True, blank=True)
    sample_type = models.TextField()
    input_payload = models.JSONField()
    expected_output = models.JSONField()
    rule_output = models.JSONField()
    llm_output = models.JSONField()
    chosen_output = models.TextField()
    is_labeled = models.BooleanField()
    label = models.TextField(null=True, blank=True)
    label_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "training_sample"


class DatasetUpload(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    dataset_type = models.TextField()
    format = models.TextField()
    source = models.TextField()
    meta = models.JSONField()
    row_count = models.TextField()
    is_processed = models.BooleanField()
    processing_error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "dataset_upload"


class SystemEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    patient_id = models.UUIDField(null=True, blank=True)
    source = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "system_event"


class ModelRouteLog(models.Model):
    id = models.UUIDField(primary_key=True)
    patient_id = models.UUIDField()
    pipeline = models.CharField(max_length=255, null=True)
    route_mode = models.CharField(max_length=255, null=True)
    rule_output = models.JSONField(null=True)
    llm_output = models.JSONField(null=True)
    chosen_output = models.CharField(max_length=255, null=True)
    diff_summary = models.JSONField(null=True)
    created_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "model_route_log"


# =========================
# DJANGO-OWNED TABLES
# =========================

class HumanLabel(models.Model):
    SAMPLE_TYPE_CHOICES = [
        ("micro", "Micro"),
        ("macro", "Macro"),
    ]

    REVIEW_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    sample_type = models.CharField(max_length=16, choices=SAMPLE_TYPE_CHOICES)
    sample_id = models.UUIDField()
    label_json = models.JSONField()
    review_status = models.CharField(
        max_length=16, choices=REVIEW_STATUS_CHOICES, default="pending"
    )
    reviewer = models.CharField(max_length=128)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "human_label"


class PromotionRequest(models.Model):
    TARGET_CHOICES = [
        ("micro", "Micro"),
        ("macro", "Macro"),
        ("rules", "Rules"),
    ]

    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("executed", "Executed"),
    ]

    target_type = models.CharField(max_length=16, choices=TARGET_CHOICES)
    target_version = models.CharField(max_length=64)
    reason = models.TextField()
    requested_by = models.CharField(max_length=128)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default="requested"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "promotion_request"

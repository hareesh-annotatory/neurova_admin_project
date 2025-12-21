from django.db import models


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

    def __str__(self):
        return f"{self.sample_type} | {self.id}"


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.event_type} | {self.severity}"


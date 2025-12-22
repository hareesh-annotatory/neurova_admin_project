#!/usr/bin/env bash
set -e

# venv must already be activated in PowerShell

python.exe manage.py check

python.exe manage.py shell -c "
from neurova_admin.models import TrainingSample, DatasetUpload, SystemEvent
print('TrainingSample_count:', TrainingSample.objects.count())
print('DatasetUpload_count:', DatasetUpload.objects.count())
print('SystemEvent_count:', SystemEvent.objects.count())
"

# Yes, by default Django signals run in the same database transaction as the caller, 
# if they are triggered within a transactional block (like during save() or create() inside a transaction).

# models.py

from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class Log(models.Model):
    message = models.CharField(max_length=255)



# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel, Log

@receiver(post_save, sender=TestModel)
def log_creation(sender, instance, **kwargs):
    Log.objects.create(message=f"Created TestModel with id {instance.id}")




# views.py

from django.db import transaction
from django.http import HttpResponse
from .models import TestModel, Log

def test_view(request):
    try:
        with transaction.atomic():
            TestModel.objects.create(name="Inside Transaction")
            raise Exception("Trigger rollback")
    except:
        pass

    logs = Log.objects.all()
    return HttpResponse(f"Log count: {logs.count()}")


# The signal creates a Log entry during post_save.
# Then we raise an exception to roll back the entire transaction.

# Output

# Copy
# Edit
# Log count: 0

# This confirms that the signal's DB action was rolled back with the main transaction,
# the signal ran in the same database transaction.


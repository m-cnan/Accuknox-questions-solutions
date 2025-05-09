# By default, Django signals are executed synchronously. 
# This means that when a signal is sent, 
# all connected signal handlers are executed immediately, 
# in the same thread, and must complete before the original operation continues.

# models.py

from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)


# signals.py

import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel

@receiver(post_save, sender=TestModel)
def slow_signal_handler(sender, instance, **kwargs):
    print("Signal handler started")
    time.sleep(5)  # Simulate delay
    print("Signal handler finished")



# views.py

from django.http import HttpResponse
from .models import TestModel

def test_view(request):
    print("Before save")
    TestModel.objects.create(name="Test")
    print("After save")
    return HttpResponse("Done")


# Output

# Before save
# Signal handler started
# (Sleep for 5 seconds...)
# Signal handler finished
# After save


# Only after the signal handler finishes, will the After save print and the HTTP response be returned.


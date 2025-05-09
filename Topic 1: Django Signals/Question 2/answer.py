# Yes, Django signals run in the same thread as the caller by default.



# signals.py

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel

@receiver(post_save, sender=TestModel)
def signal_handler(sender, instance, **kwargs):
    print(f"[Signal Handler] Thread ID: {threading.get_ident()}")




# views.py

import threading
from django.http import HttpResponse
from .models import TestModel

def test_view(request):
    print(f"[View] Thread ID: {threading.get_ident()}")
    TestModel.objects.create(name="Test")
    return HttpResponse("Done")


# When you hit the /test/ view:

# [View] Thread ID: 139921664554752
# [Signal Handler] Thread ID: 139921664554752


# The thread ID is the same, proving that:
# The signal handler runs in the same thread as the code that triggered it.
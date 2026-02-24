import threading
import os
import django
from config.wsgi import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def run_worker():
    from django.core.management import call_command
    call_command("push_updates")

threading.Thread(target=run_worker, daemon=True).start()


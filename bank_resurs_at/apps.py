from django.apps import AppConfig
from django.core.management import call_command
import threading
import os

class BankResursAtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank_resurs_at'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        def start_push():
            call_command('push_updates')

        thread = threading.Thread(target=start_push, daemon=True)
        thread.start()

TEMPLATES = [
{
 'APP_DIRS': True,
}
]
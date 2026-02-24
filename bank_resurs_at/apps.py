from django.apps import AppConfig
from django.core.management import call_command
import threading
import os

class BankResursAtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank_resurs_at'


TEMPLATES = [
{
 'APP_DIRS': True,
}
]
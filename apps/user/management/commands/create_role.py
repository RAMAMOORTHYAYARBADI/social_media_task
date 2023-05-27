import logging
from pydoc import Helper
from django.core.management.base import BaseCommand, CommandError
from apps.user import models
logger = logging.getLogger( __name__ )

class Command(BaseCommand):
    help = "Command to create a User Roles"
    def handle(self, *args, **options):
        try:
            """create user roles in Role master table"""
            roles = ["SuperAdmin","User"]
            for i in roles:
                val = models.Role.objects.update_or_create(role_name=i)
        except Exception as e:
            logger.info('command not works',e)
            raise CommandError(e)
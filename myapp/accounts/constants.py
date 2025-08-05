from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Rolechoice(TextChoices):
    ADMIN = 'admin', _('Admin')
    MANAGER = 'manager', _('Manager')
    EMPLOYEE = 'employee', _('Employee')
    


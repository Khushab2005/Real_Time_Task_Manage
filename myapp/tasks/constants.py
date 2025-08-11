from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

# ----------------
# Constants for Task Priority and Status Choices
# ----------------



class PriorityChoice(TextChoices):
    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    HIGH = 'high', _('High')
    
class StatusChoice(TextChoices):
    PENDING = 'pending', _('Pending')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')
    

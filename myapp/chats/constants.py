from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Roomchoice(TextChoices):
    SINGLE = 'single', _('Single')
    GROUP = 'group', _('Group')
    
    
    


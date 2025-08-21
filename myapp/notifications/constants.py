from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _ 


#------------------
#Notification Type Choice 
#------------------

class NotificationType(TextChoices):
    TASKS_ASSIGN = 'tasks_assign', _('Tasks_Assign')
    TASKS_COMPLETED = 'tasks_completed' , _('Tasks_Completed')
    TASKS_PENDING = 'tasks_pending' , _('Tasks_Pending')
    TASKS_MODIFY = 'tasks_modify' , _('Tasks_Modify')
    SYSTEM_ALERT =  'system_alert' , _('System_Alert')
    OTHER = 'other' , _('Other')
    
     



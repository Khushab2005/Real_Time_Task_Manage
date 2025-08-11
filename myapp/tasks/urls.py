from django.urls import path
from myapp.tasks.views import TaskAttachmentDeleteView,TaskCreateView , TaskAssignedView , TaskModifyView , TaskAttachmentView,TaskAttchmentModifyView , TaskDeleteView
 
urlpatterns = [
    # ------------------ALL TASK URLS------------------
    path('created_tasks/', TaskCreateView.as_view(), name='created_tasks'),
    path('assigned_tasks/', TaskAssignedView.as_view(), name='assigned_tasks'),
    path('modify/<int:pk>/', TaskModifyView.as_view(), name='task_detail'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    # ------------------TASK ATTACHMENT URLS------------------
    path('attachment/', TaskAttachmentView.as_view(), name='task_Attachment'),
    path('attachment_modify/<int:pk>/', TaskAttchmentModifyView.as_view(), name='task_Attachment_modify'),
    path('attachment_delete/<int:pk>/', TaskAttachmentDeleteView.as_view(), name='task_Attachment_delete'),
]
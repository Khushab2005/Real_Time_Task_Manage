from django.urls import path
from myapp.notifications.views import NotificationCreateView , NotificationListView,NotificationReadView

urlpatterns = [
    # ---------------------notification list url -------------
    path('notificationlist/',NotificationListView.as_view(),name='notification_list'),
    # ---------------------notification create url -------------
    path('notificationcreate/',NotificationCreateView.as_view(),name='notification_create'),
    # ---------------------notification read url -------------
    path('notificationread/<int:pk>/',NotificationReadView.as_view(),name='notification_read'),
]
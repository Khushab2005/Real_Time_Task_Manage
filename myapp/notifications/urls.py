from django.urls import path
from myapp.notifications.views import  NotificationListView,NotificationReadView , AnalyticsView

urlpatterns = [
    # ---------------------notification list url -------------
    path('notificationlist/',NotificationListView.as_view(),name='notification_list'),
    # ---------------------notification read url -------------
    path('notificationread/<int:pk>/',NotificationReadView.as_view(),name='notification_read'),
    # ---------------------Analytics list url -------------
    path('analytics/<int:pk>/',AnalyticsView.as_view(),name='analytics'),
]
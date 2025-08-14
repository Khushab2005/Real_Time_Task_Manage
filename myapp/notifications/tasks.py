# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from myapp.tasks.models import Task
from myapp.tasks.constants import StatusChoice
from datetime import date

@shared_task
def send_email_task(to_email, subject, text_message, html_message=None):
    if not to_email:
        return
    send_mail(
        subject,
        text_message,                 
        settings.EMAIL_HOST_USER,
        [to_email],
        html_message=html_message,    
        fail_silently=False,
    )

@shared_task
def daily_task_reminder():
    tasks = Task.objects.filter(status__in=[StatusChoice.IN_PROGRESS, StatusChoice.PENDING])
    
    for task in tasks:
        if task.assigned_to and task.assigned_to.email:
            days_left = (task.due_date - date.today()).days
            if days_left == 0:
                due_status = "Today is the last date to complete this task."
            elif days_left == 1:
                due_status = "Tomorrow is your last date to complete this task."
            elif days_left < 0:
                due_status = f"Task is overdue by {-days_left} day(s)!"
            else:
                due_status = f"{days_left} days left until due date."
            
            
            text_message = (
                f"Task Reminder\n\n"
                f"Title: {task.title}\n"
                f"Description: {task.description}\n"
                f"Due Date: {task.due_date}\n"
                f"Status: {task.get_status_display()}\n"
                f"Note: {due_status}\n"
            )
            html_message = f"""
            <!doctype html>
            <html>
              <body>
                <h3 style="margin:0 0 12px">Task Reminder</h3>
                <table cellpadding="8" cellspacing="0" border="1" style="border-collapse:collapse;width:100%">
                  <tr><th align="left">Title</th><td>{task.title}</td></tr>
                  <tr><th align="left">Description</th><td>{task.description}</td></tr>
                  <tr><th align="left">Due Date</th><td>{task.due_date}</td></tr>
                  <tr><th align="left">Status</th><td>{task.get_status_display()}</td></tr>
                  <tr><th align="left" style="background-color:yellow">Status</th><td style="background-color:yellow">{due_status}</td></tr>
                </table>
              </body>
            </html>
            """
            send_email_task.delay(task.assigned_to.email, "Task Reminder", text_message, html_message)

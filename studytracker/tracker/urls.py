from django.urls import path
from .views import add_subject, add_task, dashboard, mark_complete

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add-subject/', add_subject, name='add-subject'),
        path('add-task/', add_task, name='add-task'),
        path('complete-task/<int:task_id>/', mark_complete, name='complete-task'),
        path('delete-task/<int:task_id>/', delete_task, name='delete-task'),
]
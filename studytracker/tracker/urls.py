from django.urls import path
from .views import add_subject, add_task, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add-subject/', add_subject, name='add-subject'),
        path('add-task/', add_task, name='add-task'),
]
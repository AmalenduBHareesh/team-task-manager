from django.contrib import admin
from django.urls import path

from taskmanager import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path(
        'create-task/',
        views.create_task,
        name='create_task'
    ),

    path(
        'edit-task/<int:id>/',
        views.edit_task,
        name='edit_task'
    ),

    path(
        'delete-task/<int:id>/',
        views.delete_task,
        name='delete_task'
    ),

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'api/tasks/',
        views.task_api,
        name='task_api'
    ),

    path(
        'api/projects/',
        views.project_api,
        name='project_api'
    ),

]
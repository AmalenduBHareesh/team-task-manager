# urls.py

from django.urls import path

from taskmanager import views


urlpatterns = [

    path('', views.home, name='home'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('create-task/', views.create_task, name='create_task'),

    path('edit-task/<int:id>/', views.edit_task, name='edit_task'),

    path('delete-task/<int:id>/', views.delete_task, name='delete_task'),

    path('create-project/', views.create_project, name='create_project'),









    
     path('createsuper/', views.create_superuser),

    

]
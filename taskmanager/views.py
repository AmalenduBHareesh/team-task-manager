from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task, Project


# SIGNUP

def signup_view(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # CHECK USER EXISTS

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect('signup')

        # CREATE USER

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'taskmanager/signup.html')


# LOGIN

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('home')

        else:

            messages.error(request, "Invalid username or password")

    return render(request, 'taskmanager/login.html')


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('login')


# HOME DASHBOARD

@login_required
def home(request):

    # ADMIN SEES ALL TASKS

    if request.user.is_superuser:

        tasks = Task.objects.all()

    # MEMBERS SEE ONLY THEIR TASKS

    else:

        tasks = Task.objects.filter(
            assigned_to=request.user
        )

    total_tasks = tasks.count()

    completed = tasks.filter(
        status='Completed'
    ).count()

    pending = tasks.filter(
        status='Pending'
    ).count()

    overdue = tasks.filter(
        status='In Progress'
    ).count()

    context = {

        'tasks': tasks,

        'total_tasks': total_tasks,

        'completed': completed,

        'pending': pending,

        'overdue': overdue,

    }

    return render(
        request,
        'taskmanager/home.html',
        context
    )


# CREATE PROJECT

@login_required
def create_project(request):

    # ONLY ADMIN

    if not request.user.is_superuser:

        return redirect('home')

    if request.method == "POST":

        Project.objects.create(

            name=request.POST['name'],

            description=request.POST['description'],

            created_by=request.user

        )

        return redirect('home')

    return render(
        request,
        'taskmanager/create_project.html'
    )


# CREATE TASK

@login_required
def create_task(request):

    # ONLY ADMIN

    if not request.user.is_superuser:

        return redirect('home')

    projects = Project.objects.all()

    users = User.objects.all()

    if request.method == "POST":

        Task.objects.create(

            title=request.POST['title'],

            description=request.POST['description'],

            project=Project.objects.get(
                id=request.POST['project']
            ),

            assigned_to=User.objects.get(
                id=request.POST['assigned_to']
            ),

            status=request.POST['status'],

            priority=request.POST['priority'],

            deadline=request.POST['deadline']

        )

        return redirect('home')

    context = {

        'projects': projects,

        'users': users

    }

    return render(
        request,
        'taskmanager/create_task.html',
        context
    )


# EDIT TASK

@login_required
def edit_task(request, id):

    task = get_object_or_404(
        Task,
        id=id
    )

    if request.method == "POST":

        task.status = request.POST['status']

        task.save()

        return redirect('home')

    return render(
        request,
        'taskmanager/edit_task.html',
        {'task': task}
    )


# DELETE TASK

@login_required
def delete_task(request, id):

    # ONLY ADMIN

    if request.user.is_superuser:

        task = get_object_or_404(
            Task,
            id=id
        )

        task.delete()

    return redirect('home')
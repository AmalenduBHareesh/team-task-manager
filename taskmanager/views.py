from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Project


# HOME
@login_required
def home(request):

    tasks = Task.objects.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    pending_tasks = tasks.filter(status='Pending').count()
    overdue_tasks = tasks.filter(status='Overdue').count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
    }

    return render(request, 'taskmanager/home.html', context)


# SIGNUP
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # prevent duplicate usernames
        if User.objects.filter(username=username).exists():

            return render(
                request,
                'taskmanager/signup.html',
                {
                    'error': 'Username already exists'
                }
            )

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

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'taskmanager/login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(request, 'taskmanager/login.html')


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('login')


# CREATE PROJECT
@login_required
def create_project(request):

    if request.method == "POST":

        name = request.POST.get('name')
        description = request.POST.get('description')

        Project.objects.create(
            name=name,
            description=description
        )

        return redirect('home')

    return render(request, 'taskmanager/create_project.html')


# CREATE TASK
@login_required
def create_task(request):

    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == "POST":

        title = request.POST.get('title')
        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        project = Project.objects.get(id=project_id)
        assigned_to = User.objects.get(id=assigned_to_id)

        Task.objects.create(
            title=title,
            project=project,
            assigned_to=assigned_to,
            status=status,
            priority=priority,
            deadline=deadline
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

    task = get_object_or_404(Task, id=id)

    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == "POST":

        task.title = request.POST.get('title')

        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')

        task.project = Project.objects.get(id=project_id)

        task.assigned_to = User.objects.get(id=assigned_to_id)

        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.deadline = request.POST.get('deadline')

        task.save()

        return redirect('home')

    context = {
        'task': task,
        'projects': projects,
        'users': users
    }

    return render(
        request,
        'taskmanager/edit_task.html',
        context
    )


# DELETE TASK
@login_required
def delete_task(request, id):

    task = get_object_or_404(Task, id=id)

    task.delete()

    return redirect('home')
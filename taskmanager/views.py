from django.shortcuts import render, redirect, get_object_or_404

from .models import Task, Project

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from datetime import date

from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import TaskSerializer, ProjectSerializer



def home(request):

    if request.user.is_superuser:

        tasks = Task.objects.all()

    else:

        tasks = Task.objects.filter(
            assigned_to=request.user
        )

    search_query = request.GET.get('search')

    status_filter = request.GET.get('status')

    if search_query:

        tasks = tasks.filter(
            title__icontains=search_query
        )

    if status_filter:

        tasks = tasks.filter(
            status=status_filter
        )

    completed_count = tasks.filter(
        status='Completed'
    ).count()

    pending_count = tasks.filter(
        status='Pending'
    ).count()

    overdue_count = tasks.filter(
        due_date__lt=date.today()
    ).exclude(status='Completed').count()

    return render(request, 'taskmanager/home.html', {

        'tasks': tasks,

        'completed_count': completed_count,

        'pending_count': pending_count,

        'overdue_count': overdue_count,
        'today': date.today(),

    })


def create_task(request):

    if not request.user.is_superuser:
        return redirect('home')

    projects = Project.objects.all()

    users = User.objects.all()

    if request.method == 'POST':

        Task.objects.create(

            title=request.POST['title'],

            description=request.POST['description'],

            status=request.POST['status'],

            due_date=request.POST['due_date'],

            project=Project.objects.get(
                id=request.POST['project']
            ),

            assigned_to=User.objects.get(
                id=request.POST['assigned_to']
            )
        )

        return redirect('home')

    return render(request, 'taskmanager/create_task.html', {

        'projects': projects,

        'users': users,

    })


def edit_task(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    task = get_object_or_404(Task, id=id)

    projects = Project.objects.all()

    users = User.objects.all()

    if request.method == 'POST':

        task.title = request.POST['title']

        task.description = request.POST['description']

        task.status = request.POST['status']

        task.due_date = request.POST['due_date']

        task.project = Project.objects.get(
            id=request.POST['project']
        )

        task.assigned_to = User.objects.get(
            id=request.POST['assigned_to']
        )

        task.save()

        return redirect('home')

    return render(request, 'taskmanager/edit_task.html', {

        'task': task,

        'projects': projects,

        'users': users,

    })


def delete_task(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    task = get_object_or_404(Task, id=id)

    task.delete()

    return redirect('home')


def signup_view(request):

    if request.method == 'POST':

        User.objects.create_user(

            username=request.POST['username'],

            password=request.POST['password']

        )

        return redirect('login')

    return render(request, 'taskmanager/signup.html')


def login_view(request):

    if request.method == 'POST':

        user = authenticate(

            request,

            username=request.POST['username'],

            password=request.POST['password']

        )

        if user:

            login(request, user)

            return redirect('home')

    return render(request, 'taskmanager/login.html')


def logout_view(request):

    logout(request)

    return redirect('login')


@api_view(['GET'])
def task_api(request):

    tasks = Task.objects.all()

    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def project_api(request):

    projects = Project.objects.all()

    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)
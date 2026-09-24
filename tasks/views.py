from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def home(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', 'all')

    tasks = Task.objects.all().order_by('-created_at')

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    completed_count = Task.objects.filter(completed=True).count()
    pending_count = Task.objects.filter(completed=False).count()
    total_count = Task.objects.count()

    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_count': total_count,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'tasks/home.html', context)


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        if title:
            Task.objects.create(
                title=title,
                description=description,
                priority=priority or 'Medium',
                due_date=due_date if due_date else None
            )

        return redirect('home')

    return render(request, 'tasks/add_task.html')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority') or 'Medium'
        task.due_date = request.POST.get('due_date') or None
        task.save()

        return redirect('home')

    return render(request, 'tasks/edit_task.html', {'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()

    return redirect('home')

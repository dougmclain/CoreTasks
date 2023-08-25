from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        order = request.GET.get('order', 'asc')  # Default ordering is ascending
        if order == 'asc':
            all_tasks = TaskList.objects.filter(manage=request.user).order_by('done')
        else:
            all_tasks = TaskList.objects.filter(manage=request.user).order_by('-done')
        
        # Save the sorting preference into the session
        request.session['task_order'] = order

        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)
    
        return render(request, 'todolist.html', {'all_tasks': all_tasks, 'order': order})


@login_required   
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
        order = request.GET.get('order', 'default_order_value')
    else:
        messages.error(request, ("Access Restricted!"))
    return redirect(f'/todolist/?order={order}')

# views.py
def your_view_function(request):
    order = request.GET.get('order')
    if order:
        request.session['task_order'] = order  # Store the preference in session
    else:
        order = request.session.get('task_order', 'asc')  # Get from session or use default

 
@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
           form.save()
        messages.success(request,("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})
    
@login_required   
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
       task.done = True
       task.save()
    else:
        messages.error(request, ("Access Restricted!"))
    
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    messages.success(request, "Task status was changed successfully!")
    return redirect('edit_task', task_id=task_id)


def index(request):
    context = {
        'index_text': "Home Page",
        }
    return render(request, 'index.html', context)

@login_required
def contact(request):
    context = {
        'contact_text': "Contact Us Page",
        }
    return render(request, 'contact.html', context)
def about(request):
    context = {
        'about_text': "About Us Page",
        }
    return render(request, 'about.html', context)

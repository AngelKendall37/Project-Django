from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import ActivityForm
from .models import Activity
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registro de usuarios
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('activity')
            except IntegrityError:
                 return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
            
        return render(request, 'signup.html', { 
                    'form': UserCreationForm,
                    "error": 'Contraseña no coinciden'
                })
@login_required
def activity(request):
    activity = Activity.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'activity.html', {
        'activity': activity
    })
    
@login_required  
def activity_completed(request):
    activity = Activity.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'activity.html', {
        'activity': activity
    })
    
@login_required
def create_activity(request):
    if request.method == 'GET':
        return render(request, 'create_activity.html', {
        'form': ActivityForm
        })
    else:
        try:
            form = ActivityForm(request.POST)
            new_Activity = form.save(commit=False)
            new_Activity.user = request.user
            new_Activity.save()
            return redirect('activity')
        except ValueError:
            return render(request, 'create_activity.html', {
        'form': ActivityForm,
        'error': 'Porfavor introdusca datos validos'
        })

@login_required
def activity_detail(request, activity_id):
    if request.method == 'GET':
        activity = get_object_or_404(Activity, pk=activity_id, user=request.user)
        form = ActivityForm(instance=activity)
        return render(request, 'activity_detail.html', {
            'activity': activity,
            'form': form
        })
    else:
        try:
            activity = get_object_or_404(Activity, pk=activity_id, user=request.user)
            form = ActivityForm(request.POST, instance=activity)
            form.save()
            return redirect('activity')
        except ValueError:
            return render(request, 'activity_detail.html', {
            'activity': activity,
            'form': form,
            'error': 'Error updating activity'
        })

@login_required
def complete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, user=request.user)
    if request.method == 'POST':
        activity.datecompleted = timezone.now()
        activity.save()
        return redirect('activity')

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, user=request.user)
    if request.method == 'POST':
        activity.delete()
        return redirect('activity')

@login_required       
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
          return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('activity')
        

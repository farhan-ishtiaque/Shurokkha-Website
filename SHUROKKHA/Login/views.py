from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserIDLoginForm
from rest_framework import viewsets
#class TaskViewSet(viewsets.ModelViewSet):
    #queryset = Task.objects.all()
    #serializer_class = TaskSerializer
@login_required
def redirect_user(request):
    user = request.user
    if hasattr(user, 'role'):
     print(user.role)
     if user.role == 'operator':
        return redirect('operator_dashboard')
     elif user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('login')  # No dashboard for other roles

def custom_login(request):
    if request.method == 'POST':
        form = UserIDLoginForm(request.POST) #post since values input
        if form.is_valid():#authtntication criterias fulfilled
            user_id = form.cleaned_data['user_id'] #after validation
            password = form.cleaned_data['password']
            try:
                user = authenticate(request, username=str(user_id), password=password)
                if user is not None and user.is_active:
                    auth_login(request, user)
                    return redirect('redirect_user')
                else:
                   form.add_error(None, 'Invalid user ID or password')

            except User.DoesNotExist:
                form.add_error(None, 'Invalid user ID or password')
    else:
        form = UserIDLoginForm()
    return render(request, 'login/login.html', {'form': form})
@login_required #if not loggedin sends to login again
def operator_dashboard(request):
    return render(request, 'login/operator_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'login/admin_dashboard.html')

@login_required
def operator_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operators = User.objects.filter(role='operator') #queryset returned by filter only of role operator
    return render(request, 'login/operator_list.html', {'operators': operators})

@login_required
def add_operator(request):
    last_user = User.objects.order_by('-id').first() #gets most recent id
    next_user_id = last_user.id + 1 if last_user else 1000 #auto deafult id by retrieving from prev ID
    if request.user.role != 'admin':
        return redirect('redirect_user')

    if request.method == 'POST': #if from submitted then
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            operator = form.save(commit=False) #object created but not saved in database yet as more changes left
            operator.role = 'operator'
            default_password = "operator123"  # Set your default password here
            operator.set_password(default_password)  #Hash the password for security
            operator.save() #wrutten to database
            return redirect('operator_list')
        else:
             print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/add_operator.html', {
        'form': form,
        'next_user_id': next_user_id
    })
@login_required
def edit_operator(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=operator)
        if form.is_valid():
            form.save()
            return redirect('operator_list')
    else:
        form = CustomUserChangeForm(instance=operator)
    return render(request, 'login/edit_operator.html', {'form': form, 'operator': operator})
@login_required
def delete_operator(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
   # Toggle operator activation status
    operator.is_active = not operator.is_active
    operator.save()

    return redirect('operator_list')

from django.contrib.auth.forms import SetPasswordForm

@login_required
def set_password(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
    if request.method == 'POST':
        form = SetPasswordForm(operator, request.POST)
        if form.is_valid():
            form.save()
            return redirect('operator_list')
    else:
        form = SetPasswordForm(operator)
    return render(request, 'login/set_password.html', {'form': form, 'operator': operator})

@login_required
def search_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')

    # Get division from search query
    division_query = request.GET.get('division')

    if division_query:
        operators = User.objects.filter(role='operator', division__iexact=division_query)
    else:
        operators = User.objects.filter(role='operator')

    # Pass division query back to template to preserve selection
    return render(request, 'login/search_list.html', {
        'operators': operators,
        'selected_division': division_query or ''
    })
# views.py
from rest_framework import viewsets
from .models import Task
from .models import TaskSerializer
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

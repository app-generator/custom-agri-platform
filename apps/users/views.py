from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.views.generic import CreateView
from apps.users.models import Profile, UserRole
from apps.users.forms import SigninForm, SignupForm, UserPasswordChangeForm, UserSetPasswordForm, UserPasswordResetForm, ProfileForm
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from apps.users.utils import user_filter

User = get_user_model()

# Create your views here.

class SignInView(LoginView):
    form_class = SigninForm
    template_name = "authentication/sign-in.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "authentication/sign-up.html"
    success_url = "/users/signin/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register"
        return context

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'authentication/password-change.html'
    form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
    template_name = 'authentication/forgot-password.html'
    form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/reset-password.html'
    form_class = UserSetPasswordForm


def signout_view(request):
    logout(request)
    return redirect(reverse('signin'))


@login_required(login_url='/users/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'segment': 'profile',
    }
    return render(request, 'dashboard/profile.html', context)


@login_required
def upload_avatar(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        user = request.user

        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar = request.FILES["avatar"]
        user.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)

def change_password(request):
    user = request.user
    if request.method == 'POST':
        if check_password(request.POST.get('current_password'), user.password):
            user.set_password(request.POST.get('new_password'))
            user.save()
            messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, "Password doesn't match!")
    return redirect(request.META.get('HTTP_REFERER'))



def user_list(request):
    filters = user_filter(request)
    user_list = User.objects.filter(**filters)
    form = SignupForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    users = paginator.page(page)

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'apps/users.html', context)


@login_required(login_url='/users/signin/')
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def user_change_password(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.set_password(request.POST.get('password'))
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


#

ROLE_INFO = {
    'ADMIN': {
        'description': 'Farm Admin info'
    },
    'FARMER': {
        'description': 'Farmer Manager info'
    },
    'ENGINEER': {
        'description': 'Engineer info'
    },
    'EXECUTIVE': {
        'description': 'Execution Personnel info'
    },
    'LOGISTIC': {
        'description': 'Logistic Personnel info'
    },
    'AUDITOR': {
        'description': 'Auditor info'
    },
    'BUYER': {
        'description': 'Buyer info'
    },
}

def select_role(request):
    user = request.user

    if request.method == 'POST':
        role = request.POST.get('role')
        user.role = role
        user.save()
        return redirect('dashboard')

    roles = []

    for value, label in UserRole.choices:
        roles.append({
            'value': value,
            'label': label,
            'description': ROLE_INFO[value]['description']
        })

    context = {
        'roles': roles,
        'title': 'Select Role'
    }

    return render(request, 'authentication/select-role.html', context)


def setting_page(request):
    context = {
        'title': 'Settings'
    }
    return render(request, 'pages/settings.html', context)


def update_profile(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user.first_name = first_name
        user.last_name = last_name

        user.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))
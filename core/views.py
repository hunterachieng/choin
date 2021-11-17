from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.contrib.auth import login


# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from leadership.models import User

from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login



class LoginView(FormView):
    """login view"""
    form_class = forms.LoginForm
    success_url = reverse_lazy('change_password')
    template_name = 'home.html'
    
    
    @csrf_exempt
    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],password=credentials['password'])

        if user is not None:
            login(self.request, user)
            if user.is_previously_logged_in==False:
                return HttpResponseRedirect(reverse_lazy('change_password'))
                
            else:
                # return HttpResponseRedirect(reverse_lazy('change_password'))
                if user.role==1:
                    print(user.role)
                    return HttpResponseRedirect(reverse_lazy('leadership-profile'))
                elif user.role==2:
                    return HttpResponseRedirect(reverse_lazy('trainer-profile'))
                elif user.role==3:
                    print(user.role)
                    return HttpResponseRedirect(reverse_lazy('student-profile'))
            
        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
        return HttpResponseRedirect(reverse_lazy('login'))




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            user.is_previously_logged_in=True
            user.save()
            if user.role==1:
                return HttpResponseRedirect(reverse_lazy('leadership-profile'))
            elif user.role==2:
                return HttpResponseRedirect(reverse_lazy('trainer-profile'))
            elif user.role==3:
                print(user.role)
                return HttpResponseRedirect(reverse_lazy('student-profile'))
        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})


def index(request):
    return render(request,'trial.html')

def Profile(request):
    return render(request,'profile.html')
def navbar(request):
    return render(request,'navbar.html')

def forbidden(request):
    return render(request,'forbidden.html')




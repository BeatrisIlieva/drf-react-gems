from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView

from django_ts_gems.accounts.forms import AppUserCreationForm, PaymentForm


UserModel = get_user_model()

def index(request):
    form = PaymentForm(request.POST or None)
    
    context = {
        'form': form,
    }
    
    if request.method == 'POST':
    
        if form.is_valid():
            form.save()
            
            return redirect(request, 'common/home.html', context)
    
    return render(request, 'common/home.html', context)

# class HomeView(TemplateView):
#     template_name = 'common/home.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'

from __future__ import absolute_import
from django.views import generic
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse_lazy
from braces import views
from talks.models import TalkList

home_page = reverse_lazy('home')

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

class SignUpView(generic.CreateView,views.AnonymousRequiredMixin,views.FormValidMessageMixin):
    form_valid_message = 'successfuly signed up'
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
         resp = super(SignUpView, self).form_valid(form)
         TalkList.objects.create(user=self.object, name='To Attend')
         return resp



class LoginView(generic.FormView,views.AnonymousRequiredMixin,views.FormValidMessageMixin):
    form_class = LoginForm
    success_url = home_page
    template_name = 'accounts/login.html'
    form_valid_message = 'succesfully logged in'
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)

            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(generic.RedirectView,views.LoginRequiredMixin,views.MessageMixin):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)
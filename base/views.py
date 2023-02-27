from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

#auth
from django.contrib.auth.views import LoginView

#mixins
from django.contrib.auth.mixins import LoginRequiredMixin # this mixin need to if we dont login it goes to login page which page you want you can put this to here 

#usercreate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Task 

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields ='__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm      #------form klassi usercreationformdan olacaq
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    
    
        



    

class TaskList(LoginRequiredMixin, ListView):
    model=Task
    context_object_name = 'tasks'
    template_name='home.html'

    #this def for every user must see his tasks 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)  # we filtered task which was this user
        context['count'] = context['tasks'].filter(complete=False).count()  # this is how much uncomplated tasks count
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains = search_input
            )

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model=Task
    context_object_name = 'task'
    template_name = 'detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model=Task
    template_name = 'create.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user   #taski elave eden adamin hazirki user oldugu
        return super(TaskCreate, self).form_valid(form) 

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    template_name = 'create.html'
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(DeleteView):
    model=Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'delete.html'
    




    
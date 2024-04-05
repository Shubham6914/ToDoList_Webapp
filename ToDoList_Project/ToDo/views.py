from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm




# this mixin will restrict the unauthenticated user to access the site we can use acc to our need that 
# which functionality should be available to unauthenticated user or which not and also we need to write 
# a login url in setting.py so that it will redirect the unautheticated user to login page 
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# NOTE :"while working with class based views make sure that you are using templates names as per django rules
# and if you want to change the name your template you need to define the name of you template in that 
# particullar view otherwise you will get a error "



# created view for individual task
class TaskList(LoginRequiredMixin,ListView):
   model = Task
   context_object_name = "tasks"
   
   
   # this function help to get a data related to  current user which is login  
   def get_context_data(self, **kwargs) :
      context =  super().get_context_data(**kwargs)
      # to get the task of a current user from database
      context['tasks'] = context['tasks'].filter(user = self.request.user)
      # to check that task is completed or not 
      context['count'] = context['tasks'].filter(completed=False).count()
      
      # adding search functionality 
      # this will get the text from the request whoch user has written in search space and then it will
      # search the database of that user and if the same task found the it will return the task 
      search_input = self.request.GET.get('search_area')
      if search_input:
         context['tasks'] = context['tasks'].filter(title__icontains = search_input)
         context['search_input'] = search_input
      return context


# created view to display details of individual task
class TaskDetail(LoginRequiredMixin,DetailView):
   model = Task
   context_object_name = 'task'
   # while using class based view keep in mind that if you want to change template name you need to chage 
   # the name of template in views as well otherwise you will get a error TemplateDoesNotExist 
   template_name = 'ToDo/task.html'
   
   

# created view to create a new Task 
class TaskCreate(LoginRequiredMixin,CreateView):
   model  = Task
   # this include all field of our model which we need when creating the new task 
   # fields = '__all__'
   
   # now we dont need all fields because current user will autmoatically assign to a task by using below
   # function 
   fields = ['title','description','completed']
   # we use success_url to define that whenever  new task will be created where it will be saved or go 
   # so in this case it will saved in task_list so we will use success_url to map this data to task_list
   # using reverse_lazy utility funtion it is basiccaly used lazily reverse the urls 
   success_url = reverse_lazy('task')
   
   
   # this function is used handle form submission 
   def form_valid(self, form):
       form.instance.user = self.request.user # to get the login user instance 
       return super(TaskCreate, self).form_valid(form)   
   
   
# created this model to update a task 
class TaskUpdate(LoginRequiredMixin,UpdateView):
   model = Task
   # fields = "__all__"
   fields = ['title','description','completed']
   success_url = reverse_lazy('task')
   
   
#  created view to delete a task 
class TaskDelete(LoginRequiredMixin,DeleteView):
   model  = Task
   context_object_name = "task"
   success_url = reverse_lazy('task')
   

# created view to login new user 
class UserLoginView(LoginView):
   template_name = 'ToDo/login.html'
   fields = '__all__'
   redirect_authenticated_user = False
   
   
   def get_success_url(self) -> str:
      return reverse_lazy('task')
   
   
   
class RegistratioinPage(FormView):
   template_name = "ToDo/register.html"
   form_class = UserCreationForm
   redirect_authenticated_user = True
   success_url = reverse_lazy('task') 
   
   
   # this function will help us to data of new registered user in databse 
   def form_valid(self, form):
      user = form.save()
      if user is not None:
         login(self.request , user)
      return super(RegistratioinPage, self).form_valid(form)
   
   #  this function will provide the functionality if a login user try to access the register page  user
   # will automatically redirect to the  main page in our case we want to redirect to "task "
   def get(self, *args, **kwargs):
      if self.request.user.is_authenticated:
         return redirect('task')
      return super(RegistratioinPage, self).get(*args, **kwargs)
   
   
   
# in django 5.0 the LogoutView has been depricated so we need to use this function 
@login_required(redirect_field_name='login')
def LogoutView(request):
   logout(request)
   return redirect('login')




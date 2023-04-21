from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall


# Create your views here.
def home(request):
    return render(request,'halls/home.html')

#dashboard
def dashboard(request):
    return render(request,'halls/dashboard.html')

#class based view for SignUp
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home') #if successful SignUp redirect to home page
    template_name = 'registration/signup.html'

    '''
    purpose : Auto Login after Sign Up (no need to login again after Sign Up)
    '''
    def form_valid(self,form):
        view = super(SignUp, self).form_valid(form) #if the new Sign Up form is valid
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1') #get the uername and password from the FORM
        user = authenticate(username= username, password=password) #if username and password is same
        login(self.request, user) #let user login 
        return view #return to the login view 

#CRUD of Hall
#class based view for CreateHall - C
class CreateHall(generic.CreateView):
    model = Hall #use Hall model
    fields = ['title']  #in Hall model only have one field
    template_name = 'halls/create_hall.html'  #go to the template that have form
    success_url = reverse_lazy('dashboard') #after success submitted redirect to home

    '''
    purpose : To Let Admin check which user create which hall object
    '''
    def form_valid(self, form):
        form.instance.user = self.request.user  #get the user
        super(CreateHall,self).form_valid(form) #if it is a valid user, admin can check which user create which hall object
        return redirect('home') #return home

#class based view for DetailHall - R
class DetailHall(generic.DeleteView):
    model = Hall  #pass the model object to template
    template_name = 'halls/detail_hall.html'

#class based view for UpdateHall - U
class UpdateHall(generic.UpdateView):
    model = Hall #passed the Hall object to template
    template_name = 'halls/update_hall.html'
    fields = ['title']  #field that want to update
    success_url = reverse_lazy('dashboard')  #after updated successfully redirect back to dashboard

#class based view for DeleteHall - D
class DeleteHall(generic.DeleteView):
    model = Hall #passed the Hall object to template
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard') #after successfully deleted redirect back to dashboard
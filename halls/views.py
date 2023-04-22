from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm


# Create your views here.
def home(request):
    return render(request,'halls/home.html')

#dashboard
def dashboard(request):
    return render(request,'halls/dashboard.html')

#add video (one method can do both GET and POST , default is GET, only put condtion == POST, will do the POST portion)
def add_video(request,pk):
    form = VideoForm() #create a form if it is GET 

    #if this is the POST 
    if request.method == 'POST':
        filled_form = VideoForm(request.POST) #get the form object from template
        if filled_form.is_valid(): #if filled_form is valid
            video = Video() #create new Video object
            video.url = filled_form.cleaned_data['url'] #put the filled_form['url'] into video obj. url
            video.title = filled_form.cleaned_data['title']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.hall = Hall.objects.get(pk=pk) #get the hall primary key
            video.save() #save the object into database

    return render(request, 'halls/add_video.html',{'form':form}) #passed the obj form to add_video.html (if it is GET)

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
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
import urllib
import requests
import os

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Create your views here.
def home(request):
    #get the last 3 of recent halls 
    recent_halls = Hall.objects.all().order_by('-id')[:3]
    
    return render(request,'halls/home.html',{'recent_halls':recent_halls})

#dashboard
def dashboard(request):
    
    halls = Hall.objects.filter(user=request.user)#get the halls from current user 


    return render(request,'halls/dashboard.html',{'halls':halls})

#add video (one method can do both GET and POST , default is GET, only put condtion == POST, will do the POST portion)
def add_video(request,pk):
    form = VideoForm() #create a form if it is GET 
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk) #get the current hall
    if not hall.user ==request.user: #if not correct user
        raise Http404 #return 404
    

    #if this is the POST 
    if request.method == 'POST':
        filled_form = VideoForm(request.POST) #get the form object from template
        if filled_form.is_valid(): #if filled_form is valid
            video = Video() #create new Video object
            video.hall = hall #get the hall id 
            video.url = filled_form.cleaned_data['url'] #put the filled_form['url'] into video obj. url
            parsed_url = urllib.parse.urlparse(video.url) #parse the url form filled_form
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v') #get the query of you tube id (eg : https://www.youtube.com/watch?v=YouTubeId) get the YouTubeId
            if video_id: #if url is correct and can get video_id
                video.youtube_id =video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={  YOUTUBE_API_KEY }')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                print(title)
                video.title = title
                video.save() #save the object into database
                return redirect('detail_hall',pk) #after added video redirect to detail_hall
            
            else: #if url is not correct and cannot get video_id
 
                # if filled_form.has_error('url'):
                #     errors = filled_form['url'].errors
                #     errors.append('Need to be a YouTube URL')
                errors = filled_form._errors.setdefault('url',ErrorList())
                errors.append('Need to be a You Tube URL')

    return render(request, 'halls/add_video.html',{'form':form, 'search_form': search_form, 'hall': hall}) #passed the obj form to add_video.html (if it is GET)

#search video from youtube 
def video_search(request):
    search_form = SearchForm(request.GET) #get the SearchForm from frontend 
    if search_form.is_valid(): #if search_form is valid
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')    
        return JsonResponse(response.json())#Response from server
    return JsonResponse({'error': 'Not able to validate form'})#Response from server


#delete video
class DeleteVideo(generic.DeleteView):
    model = Video
    template_name = 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')



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
        return redirect('dashboard') #return home

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
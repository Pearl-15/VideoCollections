from .models import Video
from django import forms

#model form
class VideoForm(forms.ModelForm):
    class Meta:
        '''
        purpose : passed the Model and Django will automatically create
        '''
        model = Video 

        #let Model to grab below fields
        fields = ['url'] 

        #make customize label for the form
        labels = {'url':'YouTube Url'}

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for Videos:')


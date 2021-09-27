from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Neighbourhood, Contact, Post

class NeighbourhoodForm(ModelForm):

    class Meta:
        model = Neighbourhood
        fields = {'name','location'}
        
    def __init__(self, *args, **kwargs):
        super(NeighbourhoodForm, self).__init__(*args, **kwargs)
        
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = {'name','email','phone_number','location', 'category'}
        
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = {'post_type','title','description'}
        
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        
        labels = {
            'first_name': 'First Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = {'first_name','other_name', 'email', 'phone_number', 'username', 'user_type','neighbourhood', 'profile_image' }
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        
        for name, field in self.fields.items():
            if name != 'profile_image':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'upload'})

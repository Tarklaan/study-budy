from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User 

class FormRoom(ModelForm):
    class Meta:
        model = Room
        fields = ( 'topic', 'name', 'description')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
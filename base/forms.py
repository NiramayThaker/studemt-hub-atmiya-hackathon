from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

""" ModelForm is a readymade form class(model) which helps creating a user input form directly 
as per the specified field in the model assigned by us"""

"""Meta class is a kind of abstract class(sub class) of ModelForm class which helps us to 
change the functionality of the ModelForm class"""

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # Will generate form for all the fiels
        fields = '__all__'    
        # And not show excluded fields in the form 
        exclude = ["host", "participants"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

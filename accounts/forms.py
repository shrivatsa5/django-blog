from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from. models import Profile
class UserRegisterForm(UserCreationForm):
	email =forms.EmailField()
	#field_of_interest=forms.CharField(max_length=50)
	#first_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), max_length=32, help_text='First name')
	
	class Meta:
		model=User
		fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email =forms.EmailField()
	
	class Meta:
		model=User
		fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
	
	class Meta:
		model=Profile
		fields=['image']


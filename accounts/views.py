from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

def suggested_username(s):
	rep_user=s
	while(User.objects.filter(username=rep_user).exists()):
		n=random.randint(1,500)
		rep_user=s+str(n)
	return rep_user

def register(request):
	if(request.method=='POST'):
		username=request.POST['username']
		email=request.POST['email']
		password1=request.POST['password1']
		password2=request.POST['password2']
		 	    
		if(password1==password2):
		        
			if(User.objects.filter(username=request.POST['username']).exists()):
				present=username
				messages.warning(request,'A user with that username already exists')
				messages.info(request, 'Suggested username'+" "+ suggested_username(present))
				return redirect('register')
				print("YES")
			elif(User.objects.filter(email=request.POST['email']).exists()):
				messages.warning(request,f'A user with that email already exists')
				return redirect('register')
			else:
				user=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password1'])
				user.save()
				messages.success(request, f'Account created successfully {username}')
				return redirect('login')
		else:
			messages.warning(request,f' The two password fields didn\'t match.')
			return redirect('register')
			
	else:
		form=UserRegisterForm()
		return render(request,'accounts/register.html',{'form':form})


@login_required
def profile(request):
	if(request.method =='POST'):
		print(request.user.email)
		email_before_updation=request.user.email
		
		u_form=UserUpdateForm(request.POST,instance=request.user)
		p_form=ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
		email_after_updation=request.POST['email']
		if(email_before_updation!=email_after_updation):
			if(User.objects.filter(email=email_after_updation).exists()):
				messages.warning(request,'This email is already taken')
				return redirect('profile')

		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.info(request,f'Profile Updated successfully.')
			return redirect('profile')
		else:
			messages.warning(request,f'This username is already taken')
			return redirect('profile')

	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(request.FILES,instance=request.user.profile)
	context={
		'u_form':u_form,
		'p_form':p_form
		}

		
	return render(request,'accounts/profile.html',context )

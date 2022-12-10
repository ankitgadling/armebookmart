from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
	return render(request, "index.html")

def signup(request):
	if request.method=='POST':
			username=request.POST['username']
			email=request.POST['email']
			pass1=request.POST['pass1']
			pass2=request.POST['pass2']
			if User.objects.filter(username=username):
				messages.error(request,"Username already exist",extra_tags='usererror')
				return redirect('signup')
			if User.objects.filter(email=email).exists():
				messages.error(request, "Email Already Registered!!",extra_tags='emailexist')
				return redirect('signup')
			if pass1!=pass2:
				messages.error(request,"Password is not matching plase re-enter your details", extra_tags='passerror')
				return redirect('signup')
			else:
				myuser= User.objects.create_user(username, email, pass1)
				myuser.save()
				messages.success(request,"Account created sucessfully", extra_tags='signup')
				return redirect('signin')

	return render(request,"signup.html")

def signin(request):
	if request.method=='POST':
		username=request.POST['username']
		pass1=request.POST['pass1']
		user=authenticate(request, username=username, password=pass1)
		if user is not None:
			login(request, user)
			username=user.username
			return redirect('home')
		else:
			messages.error(request, "username or password is invalid", extra_tags='invalidcred')
			return redirect('signin')
	return render(request,"signin.html")

def signout(request):
	logout(request)
	return redirect('home')

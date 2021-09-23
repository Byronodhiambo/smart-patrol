from django.shortcuts import  render, redirect
from django.contrib.auth import login as dj_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import NewUserForm






def homepage(request):
    return render(request, 'accounts/homepage.html')

def get_help(request):
    return render(request, 'accounts/get_help.html')

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			dj_login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("accounts:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, "accounts/register.html", context={"form":form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request, user, f"You are now logged in as {username}.")
                return redirect("accounts:homepage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "accounts/login.html", context={"form":form})



@login_required
def logout(request):
    django_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("accounts:login")

@login_required
def profile(request):
    u = User.objects.get(username=request.user.username)

    prof_phone = u.profile.phone_number
    prof_estate = u.profile.estate
    prof_assigned = u.profile.assigned_area
    prof_pic = u.profile.profile_pic
    context = {
        'prof_pic':prof_pic,
        'prof_phone':prof_phone,
        'prof_estate':prof_estate,
        'prof_assigned':prof_assigned
    }
    print(prof_pic)
    return render(request, "accounts/profile.html", context)

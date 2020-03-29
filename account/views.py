from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,RegistrationForm,UserProfileForm
from .models import UserProfile,UserInfo

def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user:
                login(request,user)
                return HttpResponse("Welcome You.You have been authenticated successfully.")
            else:
                return HttpResponse("Sorry.Your username or password is not right.")
        else:
            return HttpResponse("Invalid login.")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request,"account/login.html",{"form":login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            print(userprofile_form)
            return HttpResponse("successfully")
        else:
            print(userprofile_form)
            return HttpResponse("sorry,you can't register.")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})

# Show personal infomation.
@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,"account/myself.html",{"user":user,"userprofile":userprofile,"userinfo":userinfo})

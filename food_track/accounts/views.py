from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib import messages, auth

# from django.contrib import auth
# Create your views here.
# class HomePageView(TemplateView):
#     template_name = 'register.html'
# def register_request(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect("main:home")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#         form = RegistrationForm()
#         return render (request=request, template_name="food_track/register.html", context={"register_form":form})
#         first_name = request.POST['first_name']
#         last_name = request.POST['first_name']
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         email = request.POST['email']

#         if password1 == password2:
#             user = User.objects.create_user(
#                 username=username,
#                 password=password1,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name
#             )
#         user.save()
#         print('user created')
#     else:
#         return render(request, 'contact.html')

def register(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'accounts/signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'accounts/register.html', {'error':'Password does not match!'})
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'accounts/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')

# def register(response):
#     if response.method == "POST":
#         form = RegistrationForm(response.POST)
#         if form.is_valid():
#             form.save()
#         # return redirect("/home")
#     else:
#         form = RegistrationForm()
#         return render(response, "register/register.html", {"form":form})
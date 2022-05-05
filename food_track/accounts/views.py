from django.shortcuts import render, redirect
from django.contrib import auth
from .models import Users

# Create your views here.


def register(request):
    if request.method == "POST":
        if request.POST['password1'] != request.POST['password2']:
            return render(
                request, 'accounts/register.html', {
                    'error': 'Password does not match!'})
        if int(request.POST['age']) < 2 or int(request.POST['age']) > 130:
            return render(
                request, 'accounts/register.html', {
                    'error': 'Invalid age.'})
        if request.POST['sex'].upper() not in ['M',"F"]:
            return render(
                request, 'accounts/register.html', {
                    'error': 'Invalid sex. Please enter "M" or "F"'})
        try:
            Users.objects.get(username=request.POST['username'])
            return render(
                request, 'accounts/register.html', {
                    'error': 'Username is already taken!'})
        except Users.DoesNotExist:
            user = Users.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                sex=request.POST['sex'],
                age=request.POST['age'])
            auth.login(request, user)
            return redirect('home')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(
                request, 'accounts/login.html', {
                    'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')

# def register(response):
#     if response.method == "POST":
#         form = RegistrationForm(response.POST)
#         if form.is_valid():
#             form.save()
#         # return redirect("/home")
#     else:
#         form = RegistrationForm()
#         return render(response, "register/register.html", {"form":form})

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
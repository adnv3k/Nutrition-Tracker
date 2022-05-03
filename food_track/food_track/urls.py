from django.contrib import admin
from django.urls import path, include

# from accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("foods.urls")),
    # path("register/", views.register, name="register"),
    # path("accounts/",  views.login, name='login')
    path('', include('accounts.urls')),
    path('', include('profiles.urls'))
]

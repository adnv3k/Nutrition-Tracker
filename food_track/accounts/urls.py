from django.urls import path, include
from . import views

urlpatterns = [
    # path('register/', views.register_request, name="register"),
    path('account/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path("profile/", views.SearchResultsView.as_view(), name="userprofile")
]
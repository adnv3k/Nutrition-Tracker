from django.urls import path, include
from. import views

urlpatterns = [
    path('register/', views.HomePageView.as_view(), name="create_account"),
    # path("profile/", views.SearchResultsView.as_view(), name="userprofile")
]
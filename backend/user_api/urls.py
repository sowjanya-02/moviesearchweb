from django.urls import path
from . import views

urlpatterns = [
	path('register', views.UserCreate.as_view(), name='account-create'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
    path('getuser', views.GetUser.as_view(), name='getuser'),
    path('addmovie', views.Addmovie.as_view(), name='addmovie'),
     path('deletemovie', views.Deletemovie.as_view(), name='deletemovie'),]
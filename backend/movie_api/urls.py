from django.urls import path
from . import views

urlpatterns = [
	path('search', views.Searchomdb.as_view(), name='searchmovie'),
	path('all', views.Getlistview.as_view(), name='getallmovies'),
    path('delmovie', views.DeletMovie.as_view(), name='deletemovie'),
	
]
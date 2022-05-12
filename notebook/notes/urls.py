from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create_note, name='create'),
    path('list/', views.NotesView.as_view(), name='list_notes'),
    path('result/', views.SearchResultsView.as_view(), name='search_results'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.LoginCustomView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_user, name='logout'),
]

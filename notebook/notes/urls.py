from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create_note, name='create'),
    path('list/', views.list_notes, name='list_notes'),
    path('result/', views.SearchResultsView.as_view(), name='search_results'),
    path('search/', views.SearchView.as_view(), name='search'),
]

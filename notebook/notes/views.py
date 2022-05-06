from datetime import timedelta, datetime

from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import CustomUserCreationForm, NotesForm, SearchForm
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Notes


class SignUpView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super().dispatch(*args, **kwargs)


def main(request):
    if request.user.is_authenticated:
        context = {
            'count': Notes.objects.filter(author=request.user).count()
        }
        return render(request, 'notes/main.html', context)
    return render(request, 'notes/main.html', {})


@login_required
def create_note(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('list_notes')
    else:
        form = NotesForm()
    return render(request, 'notes/create.html', {'form': form})


@login_required
def list_notes(request):
    context = {
        'notes': Notes.objects.filter(author=request.user).order_by('-created_date')
    }
    return render(request, 'notes/list_notes.html', context)


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'notes/search.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = self.form_class(user=request.user)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('login')


class SearchResultsView(ListView):
    model = Notes
    template_name = 'notes/search_results.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query = self.request.GET.get('text_search')
            d_mx = self.request.GET.get('datemax')
            d_mn = self.request.GET.get('datemin')
            cat = self.request.GET.get('cat_search')
            d_mx_clear = datetime.strptime(d_mx, "%Y-%m-%d") + timedelta(days=1)
            if cat == '':
                object_list = Notes.objects.filter(
                    author=self.request.user, text__icontains=query, created_date__range=(d_mn, d_mx_clear)
                ).order_by('-created_date')
            else:
                object_list = Notes.objects.filter(
                    author=self.request.user, text__icontains=query, created_date__range=(d_mn, d_mx_clear),
                    category=cat
                ).order_by('-created_date')
            return object_list
        else:
            raise Http404

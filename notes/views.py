from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, NotesForm
from django.views.generic.edit import CreateView
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

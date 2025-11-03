from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm, AgendaForm
from core.models import Agenda
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def create_contact(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_contacts')
    else:
        form = AgendaForm()
    return render(request, 'create_contact.html', {'form': form})


@login_required
def list_contacts(request):
    contacts = Agenda.objects.all().order_by('nome_completo')
    return render(request, 'list_contacts.html', {'contacts': contacts})


@login_required
def update_contact(request, contact_id):
    contact = get_object_or_404(Agenda, id=contact_id)
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('list_contacts')
    else:
        form = AgendaForm(instance=contact)
    return render(request, 'update_contact.html', {'form': form, 'contact': contact})


@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Agenda, id=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('list_contacts')
    return redirect('list_contacts')
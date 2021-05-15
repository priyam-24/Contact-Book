from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',"user"])
def index(request):
    user = request.user
    cust = user.customer
    contacts = UserContacts.objects.all()
    mycontacts = contacts.filter(customer=cust)
    search_input = request.GET.get('search-area')
    if search_input:
        mycontacts = UserContacts.objects.filter(full_name__icontains=search_input)
    else:
        contacts = UserContacts.objects.all()
        search_input = ''
    context={'contacts': mycontacts, 'search_input': search_input}
    return render(request, 'index.html', context)

@unauthorized_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'username or password is invalid')
    return render(request,'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthorized_user
def registerPage(request):
    form=createUserForm()
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='user')
            user.groups.add(group)
            email=form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=username,email=email)
            messages.success(request,'Account created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',"user"])
def addContact(request):
    user = request.user
    cust = user.customer
    if request.method == 'POST':

        new_contact = UserContacts(
            customer=cust,
            full_name=request.POST['fullname'],
            relationship=request.POST['relationship'],
            email=request.POST['email'],
            phone_number=request.POST['phone-number'],
            address=request.POST['address'],
            )
        
        new_contact.save() 
        return redirect('/')

    return render(request, 'new.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',"user"])
def editContact(request, pk):
    contact = UserContacts.objects.get(id=pk)

    if request.method == 'POST':
        contact.full_name = request.POST['fullname']
        contact.relationship = request.POST['relationship']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone-number']
        contact.address = request.POST['address']
        contact.save()

        return redirect('/profile/'+str(contact.id))
    return render(request, 'edit.html', {'contact': contact})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',"user"])
def deleteContact(request, pk):
    contact = UserContacts.objects.get(id=pk)

    if request.method == 'POST':
        contact.delete()
        return redirect('/')

    return render(request, 'delete.html', {'contact': contact})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',"user"])
def contactProfile(request, pk):
    contact = UserContacts.objects.get(id=pk)
    return render(request, 'contact-profile.html', {'contact':contact})
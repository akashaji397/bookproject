from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth.models import User
from .models import UserProfile,loginTable


def index(request):
    return render(request,'admin_step/index.html')

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import UserProfile, loginTable  # Ensure your models are imported

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, loginTable  # Assuming loginTable is defined elsewhere

def UserRegistration(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This username already exists!')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This email is already taken')
            return redirect('register')

        # Check if passwords match
        if password != password1:
            messages.info(request, 'Passwords do not match.')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
        user.save()

        # Create a corresponding UserProfile instance using username instead of user
        UserProfile.objects.create(username=username, firstname=firstname, lastname=lastname, email=email, password=password, password1=password1)

        # Create login table entry
        login_table = loginTable(username=username, password=password, type='user')
        login_table.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'auth/register.html')




def loginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=loginTable.objects.filter(username=username,password=password,type='user').exists()

        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='user':
                    request.session['username']=user_name
                    return redirect('user_view')
                elif type=='admin':
                    request.session['username']=user_name
                    return redirect('listBook')
            
            else:
                messages.error(request,'invalid username or password')
        except:
            messages.error(request,'invalid role..')
    return render(request,'auth/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')

    
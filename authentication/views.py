from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserRole, ApplicationUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import View


def login_view(request):
    if request.method == 'POST':
        if(not request.user.is_authenticated):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if(user is not None):
                login(request, user)
                #it will fetch the corresponding user from the ApplicationUser model
                appuser = user.appusers
                if(appuser.roles.filter(name="Admin").exists()):
                    return redirect('admin_home')
                elif(appuser.roles.filter(name="User").exists()):
                    return redirect('user_home')
                else:
                    return HttpResponse('No roles matched')
                    
            else:
                return HttpResponse('failed to authenticate')
        else:
            return HttpResponse('User Already Authenticated')
    else:
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            
            if(user is not None):
                appuser = ApplicationUser(user=user)
                role = UserRole.objects.get(name="User")
                print('Roles getting succesfull', role)
                appuser.save()
                appuser.roles.add(role)
                appuser.save()

                login(request, user)
                return HttpResponse("logged in sucessfully")
            else:
                return HttpResponse('failed to authenticate')
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return render(request, 'register.html')


def logout_view(request):
    if(request.user.is_authenticated):
        logout(request=request)
        return redirect('login')
    else:
        return redirect('login')


def admin_home(request):
    if(request.user.is_authenticated):

        appuser = request.user.appusers
        data = {
            'role': 'admin'
        }
        if(appuser.roles.filter(name="Admin").exists()):
            data['role'] = 'admin'
        else:
            data['role'] = 'user'

        return render(request, 'admin_home.html', {'role':data['role']})
    else:
        return redirect('login')


def user_home(request):
    if(request.user.is_authenticated):
        appuser = request.user.appusers
        print(appuser)
        data = {
            'role': 'admin'
        }
        if (appuser.roles.filter(name="Admin").exists()):
            data['role'] = 'admin'
        else:
            data['role'] = 'user'
        return render(request, 'user_home.html', {'role':data['role']})
    else:
        return redirect('login')

class ResetPasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'reset_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('login.html')
        else:
            print(form.errors)
            return render(request, 'reset_password.html', {'form': form})
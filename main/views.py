from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "main/index.html")
    else:
        return render(request, 'main/index.html')


def answer(request):
    return render(request, 'main/answer.html')


def post(request):
    return render(request, 'main/post.html')


def contact(request):
    return render(request, 'main/contact.html')


def userlogin(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    if request.method == 'GET':
        return render(request, 'account/login.html')

    elif request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = authenticate(request, username=name, password=password)
        user.save()
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return JsonResponse({'msg': 'Invalid username and password'})
    

def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    # if request.user.is_authenticated:
    #     return redirect()

    if request.method == 'GET':
        return render(request, 'account/register.html')

    elif request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username_count = User.objects.filter(username=name).count()
        email_count = User.objects.filter(email=email).count()

        if username_count > 0:
            return JsonResponse({'msg': 'This username is in used'})

        if email_count > 0:
            return JsonResponse({'msg': 'This email is in used'})

        if password1 == password2:

            User.objects.create_user(
                username=name, email=email, password=password1)
            return JsonResponse({'msg': 'Account created Sucessfully!'})
        else:
            return JsonResponse({'msg': 'password did not match'})

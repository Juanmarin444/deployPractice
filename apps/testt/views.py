from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'testt/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw.decode('utf-8')
        )
        messages.info(request, 'You have successfully registered.')
        my_user = User.objects.get(id = user.id)
        request.session['user_id'] = my_user.id

        return redirect('/success')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if 'user' in errors:
            request.session['user_id'] = errors['user'].id
            return redirect('/success')
        else:
            for tag, error in errors.items():
                messages.error(request, error, extra_tag=tag)
                return redirect('/')

def success(request):
    logged_user = User.objects.get(id = request.session['user_id'])
    context = {
        'logged_user': logged_user
    }
    return render(request, 'testt/success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

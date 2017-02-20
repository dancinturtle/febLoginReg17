from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(req):
    return render(req, 'reg/index.html')

def login(req):
    if req.method == 'POST':
        validate = User.objects.login(req.POST)
        print "login data received", validate
        if validate[0] == False:
            loginMessages = {'absent': 'This email could not be located in our database', 'password': 'The password you entered is incorrect.'}
            for problem in validate[1]:
                messages.error(req, loginMessages[problem], extra_tags = "login")
            return redirect('/')
        req.session['loggedin'] = validate[1].id
        return redirect('/success/{}'.format(validate[1].id))
    else:
        return redirect('/')

def register(req):
    if req.method == 'POST':
        validate = User.objects.register(req.POST)
        if validate[0] == False:
            assignMessages = {'empty': "All fields are required",
              'name': "First and last names must contain at least two characters and be composed only of letters",
              'email': "Invalid email entered",
              'passlength':"Password must contain at least 8 characters",
              'passmatch': "Passwords must match",
              'unique': "Email has already been taken",
              'birthday': "Birthday must be in the past",
              'young': "You must be at least ten years old to register"}
            if len(validate[1])>0:
                for problem in validate[1]:
                    messages.error(req, assignMessages[problem], extra_tags = "register {}".format(problem))
                messages.info(req, req.POST['first_name'], extra_tags="firstname")
                messages.info(req, req.POST['last_name'], extra_tags="lastname")
                messages.info(req, req.POST['email'], extra_tags="email")
                messages.info(req, req.POST['birthday'], extra_tags="birthday")
            return redirect('/')

        print "Sucessful registration", validate[1].id
        req.session['loggedin'] = validate[1].id
        return redirect('/success/{}'.format(validate[1].id))
    else:
        return redirect('/')

def success(req, id):
    if 'loggedin' not in req.session:
        messages.error(req, "You must be logged in to view the requested page", extra_tags = 'login')
        return redirect('/')
    if int(req.session['loggedin']) != int(id):
        messages.error(req, "You are not permitted to view the requested page", extra_tags = 'login')
        return redirect('/')
    context = {'guest':User.objects.get(id=id)}

    return render(req, 'reg/success.html', context)

def logout(req):
    req.session.clear()
    messages.success(req, "You have been logged out", extra_tags = 'login')
    return redirect('/')

from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
from datetime import date, datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        print "The provided birthday", postData['birthday']
        minage = timedelta(days = 365*10)
        try:
            converted = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            print "converted", converted
            if converted >= datetime.now():
                errors.append('birthday')
            elif datetime.now() - converted < minage:
                errors.append('young')
        except:
            pass
        nameRegex = re.compile(r'^[a-zA-Z]{2,}$')
        emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        #check that everything's filled out
        for item in postData:
            if len(postData[item])<1:
                errors.append("empty")
                break
        try:
            foundguest = User.objects.get(email = postData['email'])
            errors.append('unique')
        except:
            pass
        valFirst = nameRegex.match(postData['first_name'])
        valSecond = nameRegex.match(postData['last_name'])
        valEmail = emailRegex.match(postData['email'])
        if valFirst == None or valSecond == None:
            errors.append("name")
        if valEmail == None:
            errors.append("email")
        if len(postData['password'])<8 or len(postData['conpassword'])<8:
            errors.append("passlength")
        if postData['password'] != postData['conpassword']:
            errors.append("passmatch")

        if len(errors)>0:
            return (False, errors)
        hashedPass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        newGuest = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], pw_hash = hashedPass, birthdate = converted)
        return (True, newGuest)


    def login(self, postData):
        errors = []
        print "Posted email", postData['email']
        try:
            foundGuest = User.objects.get(email = postData['email'])
            print "Found the guest", foundGuest
            if bcrypt.hashpw(postData['password'].encode(), foundGuest.pw_hash.encode()) == foundGuest.pw_hash:
                return (True, foundGuest)
            else:
                errors.append('password')
                return (False, errors)
        except:
            errors.append('absent')
            return (False, errors)


class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    pw_hash = models.CharField(max_length = 200)
    birthdate = models.DateField(auto_now = False, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

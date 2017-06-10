from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg_fn_validation(self, postData):
        errors = []
        # //name validate
        if len(postData['name'])< 2 or not postData['name'].isalpha():
            errors.append('name: Letters only and No fewer than 2 characters.')
        # //alios validate
        if len(postData['alios'])< 2 or not postData['alios'].isalpha():
            errors.append('alios: Letters only and No fewer than 2 characters.')
        # //email validate
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('EMAIL is NOT validate.')
        elif len(User.objects.filter(email=postData['email'])) != 0:
            errors.append('EMAIL has been registered.')
        # //password validate
        if len(postData['password']) < 8:
            errors.append('password not less than 8 characters.')
        elif postData['password'] != postData['confirm']:
            errors.append('password not match.')
            # return 'errors'

        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            # print hashed_pw + "STORED HASH"
            d = User.objects.create(name=postData['name'], alios=postData['alios'], email=postData['email'], password=hashed_pw, date_birth = postData['date_birth'])
            return [True, d]

        else:
            # print errors
            # return [False, False]
            return errors
    def login_check(self, postData):
        errors = []
        # check email exist
        if postData['email']=='':
            errors.append('Please insert a user!')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('EMAIL is NOT validate.')
        elif User.objects.filter(email=postData['email']).count()==0:
            errors.append('User is not exist!')
        elif len(postData['password'])==0:
                errors.append('Please insert password!')
        # check pw
        else:
            stored_hash = User.objects.get(email=postData['email']).password
            input_hash = bcrypt.hashpw(postData['password'].encode(), stored_hash.encode())
        # print input_hash + "INPUT HASH"
            if stored_hash != input_hash:
                errors.append('Incorrect password!')
        if len(errors) == 0:
            return True
        else:
            # print errors
            return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    alios = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return 'id: '+ str(self.id) + ' name: '+ self.name + ' alios: ' + self.alios + ' email: ' + self.email + 'password: ' + self.password + '    date_birth: ' + str(self.date_birth)

class Quote(models.Model):
    text = models.TextField(max_length=1000)
    user = models.ForeignKey(User, related_name='quotes')
    user_who_quoted = models.ManyToManyField(User, related_name = 'favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def first_name_validator(self, postData):
        errors = []
        if len(postData['first_name']) <2:
            errors.append({'tag': 'first_name', 'message': "First name needs to be longer than 2 charaters!" })
        return errors

    def last_name_validator(self, postData):
        errors = []
        if len(postData['last_name']) <2:
            errors.append({'tag': 'last_name', 'message': "Last name needs to be longer than 2 charaters!" })
        return errors

    def email_validator(self, postData):
        errors = []
        print(EMAIL_REGEX.match(postData['email']))
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 8:
            errors.append({'tag': 'email', 'message': "email needs to be in the correct format and over 8 charaters!" })
        else: 
            user_list = User.objects.filter(email = postData['email']) #return list of users
            if len(user_list) > 0:
                errors.append({'tag': 'email', "message": "Email already exist, try logging in instead"})
        return errors

    def password_validator(self, postData):
        errors = []
        if len(postData['password']) < 8:
            errors.append({'tag': 'password', 'message': "password needs to be longer than 8 charaters!" })
        elif postData['password_conf'] != postData['password']:
                errors.append({'tag': 'password_conf', 'message': "password confirmation is not equil to password!" })
        return errors

    def update_validator(self, postData):
        errors = []
        if len(postData['first_name']) <2:
            errors.append({'tag': 'first_name', 'message': "First name needs to be longer than 2 charaters!" })

        if len(postData['last_name']) <2:
            errors.append({'tag': 'last_name', 'message': "Last name needs to be longer than 2 charaters!" })

        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 8:
            errors.append({'tag': 'email', 'message': "email needs to be in the correct format and over 8 charaters!" })
        else: 
            user_list = User.objects.filter(email = postData['email']).exclude(email=postData['email']) #return list of users
            if len(user_list) > 0:
                errors.append({'tag': 'email', "message": "Email already exist, try logging in instead"})
        return errors


class DateManager(models.Manager):
    def title_validator(self, postData):
        errors = []
        if len(postData['title']) < 3:
            errors.append({'tag': 'title', 'message': "Title needs to be longer than 3 characters!" })
        return errors

    def desc_validator(self, postData):
        errors =[]
        if len(postData['desc']) < 10:
            errors.append({'tag': 'desc', 'message': "Description needs to be longer than 10 characters!" })
        return errors

    def loc_validator(self, postData):
        errors =[]
        if len(postData['loc']) < 10:
            errors.append({'tag': 'loc', 'message': "Location needs to be longer than 10 characters!" })
        return errors

    def update_edit_validator(self, postData):
        errors = []
        if len(postData['title']) < 3:
            errors.append({'tag': 'title', 'message': "Title needs to be longer than 3 characters!" })
        
        if len(postData['desc']) < 10:
            errors.append({'tag': 'desc', 'message': "Description needs to be longer than 10 characters!" })

        if len(postData['loc']) < 10:
            errors.append({'tag': 'loc', 'message': "Location needs to be longer than 10 characters!" })
        return errors




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hash_pw =models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects = UserManager()

class Date(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    loc = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="date_creators", on_delete=models.CASCADE)
    joiners = models.ManyToManyField(User, related_name=("joineddate"))
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects = DateManager()
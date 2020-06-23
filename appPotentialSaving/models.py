from django.db import models
import re
import bcrypt
from datetime import datetime

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):

    def regEntryValidate(self,reqpost):
        errors={}
        if len(reqpost['firstnm'])<2:
            errors['firstnm'] = 'First Name: Min 2 Characters Please'
        if len(reqpost['lastnm'])<2:   
            errors['lastnm'] = 'Last Name: Min 2 Characters Please'
        if not email_regex.match(reqpost['email']):
            errors['email'] = 'Email: Missing / Wrong Format?'
        if len(reqpost['pswd']) < 8:
            errors['pswd'] = 'Password: Min 8 Characters Please'
        if reqpost['cfpswd'] != reqpost['pswd']:
            errors['cfpswd'] = 'Confirm Password: Not Matching Password'
        return errors

    def regExistValidate(self,reqpost):  
        errors={}
        emailAlready = User.objects.filter(email=reqpost['email']).first()
        if emailAlready:
            errors['email'] = "Email Already Exists - Please Login"
        return errors

    def loginValidate(self,reqpost):
        errors={}
        if reqpost['email']=="":
            errors['email'] = 'Email: Missing at Login'
        elif not email_regex.match(reqpost['email']):
            errors['email'] = 'Email: Incorrect Format at Login'
        else:
            #check emailIsFound
            emailIsFound = User.objects.filter(email=reqpost['email']).first()
            if not emailIsFound:
                errors['emailNotFound'] = 'Email: Not Exist at Login - Please Register'
            else:
                # check hashedpw
                # # debug
                # print("*-"*20+"\n"+userFound.firstnm)  
                # validate pswd (input pswd, db-stored pswd)
                pswdMatch = bcrypt.checkpw(reqpost['pswd'].encode(),emailIsFound.pswd.encode())
                if not pswdMatch:
                    errors['pswdNotMatch'] = "Password: Incorrect at Login"
        return errors

class User(models.Model):
    firstnm = models.CharField(max_length=50)
    lastnm = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    pswd = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"\n*****\nFirst: {self.firstnm}\nLast: {self.lastnm}\nEmail: {self.email}\nPswd: {self.pswd}\nCreated: {self.created_at}"

##########################################################################################################################################################################
##########################################################################################################################################################################
# python manage.py shell
# from appPotentialSaving.models import *


class ItemManager(models.Manager):

    def itemEntryValidate(self,reqpost):
        errors={}
        if reqpost['name']=="":
            errors['name'] = 'What is the item?'
        # if reqpost['price']=="":
        #     errors['price'] = "Price shouldn't be blank!"
        
        return errors

    # decided NOT to implement existing item validation to make the list flexible
    # in case users want to keep track
    # def itemExistValidate(self,reqpost):  
    #     errors={}
    #     enteredItem = reqpost['name'].title()
    #     print("`"*40)
    #     print(enteredItem)
    #     print(datetime.today())
    #     # itemExistAlready = Item.objects.filter(name=enteredItem).first()
    #     itemExistAlready = Item.objects.filter(name=enteredItem,created_at=datetime.today()).first()  ###  ??? datetime.today() ???
    #     if itemExistAlready:
    #         errors['itemExist'] = "Item Already Exist - Please select from listing below"
    #     return errors


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4,decimal_places=2,default=0.00)        # price = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    isCompleted = models.BooleanField(default=False)
    isSaved = models.BooleanField(default=False)
    neededBy = models.ManyToManyField(User,related_name="needs")

    def __repr__(self):
        prin
        return f"\n~~~~~~~\nItem: {self.name}\nCreatedAt: {self.created_at}\nPrice: {self.price}\nCompleted: {self.isCompleted}\nSaved: {self.isSaved}"


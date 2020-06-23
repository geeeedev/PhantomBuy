from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request,'index.html')

#####################################################################################
# register user
#####################################################################################

def register(request):
    # check input errors
    errors = User.objects.regEntryValidate(request.POST)
    if len(errors)>0:
        for k,eMsgs in errors.items():
            messages.error(request,eMsgs)
        return redirect('/')

    # check userExists
    errors = User.objects.regExistValidate(request.POST)
    if len(errors)>0:
        for k,eMsgs in errors.items():
            messages.error(request,eMsgs)    
        return redirect('/')
    else:
        # hash pswd
        hashedPW = bcrypt.hashpw(request.POST['pswd'].encode(),bcrypt.gensalt()).decode()
        # create user in DB
        newUser = User.objects.create(firstnm=request.POST['firstnm']
                            ,lastnm=request.POST['lastnm']
                            ,email=request.POST['email']
                            ,pswd=hashedPW)
        # save newUser in session
        request.session['currUserID'] = newUser.id
        return redirect('/dashboard')


def login(request):
    # validate email/user exists/pswd
    errors = User.objects.loginValidate(request.POST)
    if len(errors)>0:
        for k,eMsgs in errors.items():
            messages.error(request,eMsgs)
        return redirect('/')
    
    loggedInUser = User.objects.filter(email=request.POST['email']).first()
    request.session['currUserID'] = loggedInUser.id
    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')



#####################################################################################
# create list
#####################################################################################

def new(request):
    # loading Add New page, grabbing all existing Items
    return render(request,"new.html")

def create(request):
    # validate Item data entry
    errors = Item.objects.itemEntryValidate(request.POST)
    if len(errors)>0:
        for k,eMsgs in errors.items():
            messages.error(request,eMsgs)
        return redirect('/sav/new')
    
    # decided not to do this to improve list flexibility
    # # validate Item preexisting entry
    # errors = Item.objects.itemExistValidate(request.POST)
    # if len(errors)>0:
    #     for k,eMsgs in errors.items():
    #         messages.error(request,eMsgs)
    #     return redirect('/sav/new')

    # create cat in db
    currUser = User.objects.filter(id=request.session['currUserID']).first()
    enteredItem = request.POST['name'].title()
    enteredPrice = request.POST['price']
    if enteredPrice == '':
        newItem = Item.objects.create(name=enteredItem)
    else:
        newItem = Item.objects.create(name=enteredItem
                                    ,price=request.POST['price'])
    newItem.neededBy.add(currUser)


    # return redirect(f'/sav/{newItem.id}')
    return redirect('/dashboard')


#####################################################################################
# show list
#####################################################################################

def success(request):
    currUserID = request.session.get('currUserID')
    if currUserID is None:
        messages.error(request,'Please Register or Login')
        return redirect('/')
    else:
        completed = Item.objects.filter(isCompleted=True,isSaved=False)         # AND without Q import
        pending = Item.objects.filter(Q(isCompleted=False),Q(isSaved=False))    # Q obj requires Q import above
        skipSaved = Item.objects.filter(isSaved=True)
        totalSaving = Item.objects.filter(isSaved=True).aggregate(Sum('price'))
        context = {
            'currUser': User.objects.get(id=currUserID),
            'completed' : completed,
            'pending' : pending,
            'skipSaved': skipSaved,
            'totalSaving' : totalSaving
        }
        return render(request,"dashboard.html",context)


### Manipulate date for testing
# oldCoffee = Item.objects.get(id=28)
# oldCoffee.created_at = datetime.strptime('2020-03-24','%Y-%m-%d')
# oldCoffee.save()


def toggleComplete(request, id):
    toggleCompleted = Item.objects.filter(id=id).first()
    toggleCompleted.isCompleted = not toggleCompleted.isCompleted
    toggleCompleted.save()
    return redirect('/dashboard')

def toggleSave(request, id):
    toggleSaved = Item.objects.filter(id=id).first()
    toggleSaved.isSaved = not toggleSaved.isSaved
    toggleSaved.save()
    return redirect('/dashboard')


def displayItems(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request,"items.html",context)


#####################################################################################
# udpate item (individual <a> link with id)
#####################################################################################

def edit(request, id):
    context = {
        'item' : Item.objects.filter(id=id).first(),
    }
    return render(request,"edit.html", context)


def update(request, id):
    # validate Item data entry
    errors = Item.objects.itemEntryValidate(request.POST)
    if len(errors)>0:
        for k,eMsgs in errors.items():
            messages.error(request,eMsgs)
        return redirect("/dashboard")

    # updateItem = Item.objects.filter(id=request.POST['id']).first() -- use id fr. route, dont need this
    updateItem = Item.objects.filter(id=id).first()
    updateItem.name = request.POST['name']
    updateItem.price = request.POST['price']
    updateItem.save()     

    return redirect("/dashboard")                     


def destroy(request, id):
    item = Item.objects.filter(id=id).first()
    item.delete()
    return redirect('/dashboard')


def destroyAll(request):
    Item.objects.all().delete()
    return redirect('/items')



#####################################################################################
# bulk update (checkbox with 1 button)
#####################################################################################

def editItemPrice(request):
    context = {
        'items' : Item.objects.all()
    }
    return render(request,"editItem.html",context)


def updateItemPrice(request):

    updateItems = request.POST.getlist("updateItems")
    print(" --   --  D E B U G  --    --    -- ")
    print(updateItems)
    for id in updateItems:
        print(request.POST[id])
        priceUpdated=Item.objects.filter(id=id).first()
        priceUpdated.price = request.POST[id]
        priceUpdated.save()

    return redirect('/items')


def bulkUpdate(request):
    if request.POST['btn']=='bulkComplete':
        bulkComplete(request)
        # print("DEBUG    --     --      --      --  ")
        # print(request.POST)
    elif request.POST['btn']=='bulkSave':
        bulkSave(request)
        # print("^^^^^^^          ")
        # print(request.POST)
    elif request.POST['btn']=='bulkDelete':
        bulkDelete(request)
    
    return redirect('/dashboard')


# 'chbxItem': ['1', '5', '7']  # format example
def bulkComplete(request):
    itemsCompleted = request.POST.getlist("chbxItem")
    # print("DEBUG    --     --      --      --  ")
    # print(itemsCompleted)
    for itemID in itemsCompleted:
        completed = Item.objects.filter(id=itemID).first()
        completed.isCompleted= not completed.isCompleted
        completed.save()

    return redirect('/dashboard')


def bulkSave(request):
    itemsSaved = request.POST.getlist("chbxItem")
    for itemID in itemsSaved:
        saved = Item.objects.filter(id=itemID).first()
        saved.isSaved = not saved.isSaved
        saved.save()

    return redirect('/dashboard')


def bulkDelete(request):
    itemsDeleted = request.POST.getlist("chbxItem")
    for itemID in itemsDeleted:
        deleted = Item.objects.filter(id=itemID).first().delete()
    
    return redirect('/dashboard')


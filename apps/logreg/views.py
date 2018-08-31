
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *


# the index function is called when root is visited
def index(request):
    #check if user is logged in
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, "logreg/index.html")

def dashboard(request):
    if 'id' not in request.session:
        return redirect ('/')
    logged_user = User.objects.get(id=request.session['id'])
    joined_dates = Date.objects.filter(joiners=logged_user)
    not_planned_dates = Date.objects.all().exclude(joiners=logged_user)
    #not_my_dates = Date.objects.all().filter(creator=logged_user).exclude(joiners=logged_user)

    return render(request, "logreg/dashboard.html", { 'joined_dates' : joined_dates, 'not_planned_dates' : not_planned_dates })


def reg(request):
    if request.method == "POST":
        errors = (
                User.objects.first_name_validator(request.POST) 
                + User.objects.last_name_validator(request.POST) 
                + User.objects.email_validator(request.POST) 
                + User.objects.password_validator(request.POST)
        )

        if len(errors) == 0:  
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], hash_pw=pw_hash)
        else: #not created
            for error in errors:
                messages.error(request, error['message'], extra_tags=error['tag'])
    return redirect('/')

def login(request):
    if request.method == "POST":
        user_list = User.objects.filter(email=request.POST['email'])
        if len(user_list) is 0:
            pass
        else:
            this_user = user_list[0]
            check_password = bcrypt.checkpw(request.POST['password'].encode(), this_user.hash_pw.encode()) #bool
            if check_password == True:
                    #put userid in session
                request.session['id'] = this_user.id
                request.session['first_name'] = this_user.first_name
                request.session['last_name'] = this_user.last_name
                request.session['email'] = this_user.email
                return redirect('/') #root will check for session
        messages.error(request, 'email password is invalid, try again', extra_tags="login")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def adddate(request):
    if 'id' in request.session:
        return render(request, 'logreg/adddate.html')  
    else:
        return redirect('/')

def process_adddate(request):
    errors = (
        Date.objects.title_validator(request.POST) #VAL
        + Date.objects.desc_validator(request.POST)
        + Date.objects.loc_validator(request.POST)
        )
    print(errors)
    if len(errors) == 0:
        date = Date.objects.create(creator = User.objects.get(id=request.session['id']), title =request.POST['title'], desc =request.POST['desc'], loc =request.POST['loc'])
        #date.creator.add(User.objects.get(id=request.session['id']))
    else:
        for error in errors:
            messages.error(request, error['message'], extra_tags=error['tag'])
    request.session['title'] = date.title
    request.session['desc'] = date.desc
    request.session['loc'] = date.loc

    return redirect('/dashboard')


def viewdate(request, date_id):
    date_list = Date.objects.filter(id=date_id)
    datejoin_list = User.objects.filter(date_creators__id=date_id) #
    return render(request, 'logreg/viewdate.html',  { "date_list" : date_list , "datejoin_list" : datejoin_list })


def joindate(request, id): #join is the add button the main page:  Selfjoin here
    user_join=User.objects.get(id=request.session['id'])
    date_join=Date.objects.get(id=id)
    date_join.joiners.add(user_join)
      
    return redirect('/dashboard') 

def cancel(request, id):  #cancel join 
    can_user_join=User.objects.get(id=request.session['id'])
    can_date_join=Date.objects.get(id=date_id)
    can_date_join.joiners.remove(can_user_join) 
    return redirect('/dashboard')
    
def delete(request, id): # deletes/DONE Date is over
    Date.objects.filter(id=id).delete()
    return redirect('/dashboard')


def process_edit(request):  #EDIT DATE
    print(request.POST)
    saved_date = Date.objects.get(id=request.POST['date_id'])
    saved_date.title = request.POST['title']
    saved_date.desc = request.POST['desc']
    saved_date.loc = request.POST['loc']
    saved_date.save()
    
    errors = Date.objects.update_edit_validator(request.POST) #
    if len(errors):
        for error in errors:
            messages.error(request, error['message'], extra_tags=error['tag'])
        return redirect('/edit')
    return redirect('/')

def edit(request, id): #edit Date
    if 'id' not in request.session:
        return redirect('/')
    edit_date = Date.objects.get(id=id)
    return render(request, 'logreg/edit.html', {'edit_date': edit_date }) 

def edituser(request):
    if 'id' not in request.session:
        return redirect('/')
    edituser = User.objects.get(id=request.session['id'])

    return render(request, 'logreg/edituser.html', {'edituser': edituser }) 

def processedituser(request):
    print(request.POST)
    saved_user = User.objects.get(id=request.session['id'])
    saved_user.first_name = request.POST['first_name']
    saved_user.last_name = request.POST['last_name']
    saved_user.email = request.POST['email']
    saved_user.save()
    
    errors = User.objects.update_validator(request.POST) #
    if len(errors):
        for error in errors:
            messages.error(request, error['message'], extra_tags=error['tag'])
        return redirect('/edituser')

    
    return redirect('/')

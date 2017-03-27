from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment


def index(request):
    return render(request, 'dashboard_app/index.html')

def login(request):
    if request.session.get('logged_in'):
        return redirect('/dashboard')
    return render(request, 'dashboard_app/login.html')

def logout(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    del request.session['logged_in']

    return redirect('/')

def register(request):
    return render(request, 'dashboard_app/register.html')

def process_registration(request):
    status, request, password_hash = User.objects.validate(request)
    print "Status: ", status
    if status:
        print "*"*50
        print "First Name: ", request.POST['f_name']
        print "Last Name: ", request.POST['l_name']
        print "Email: ", request.POST['email']
        print "Hash: ", password_hash
        if not User.objects.filter(level=9):
            level = 9
        else:
            level = 8
        print "User Level: ", level
        print "*"*50
        User.objects.create(f_name=request.POST['f_name'], l_name=request.POST['l_name'], email=request.POST['email'], pwh=password_hash, level=level)
        messages.success(request, "You have successfully registered.  Please login!")
        return redirect('/login')
    else:
        return redirect('/register')

def admin(request):
    if not request.session.get('logged_in'):
        return redirect('/')

    if request.session['level'] != 9:
        return redirect('/dashboard')

    context = {
    'users' : User.objects.all(),
    }

    return render(request, 'dashboard_app/admin.html', context)

def admin_edit(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.session['level'] !=9:
        return redirect('/users/edit')

    context = {
    'user' : User.objects.get(id=id),
    }

    return render(request, 'dashboard_app/admin_edit.html', context)


def newuser(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    return render(request, 'dashboard_app/newuser.html')

def edit(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    context = {
    'user' : User.objects.get(id=request.session['id']),
    }

    return render(request, 'dashboard_app/edit.html', context)

def update(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    id=request.session['id']
    if User.objects.validate_update(request,id):
        update_object=User.objects.get(id=request.session['id'])
        update_object.f_name=request.POST['f_name']
        update_object.l_name=request.POST['l_name']
        update_object.email=request.POST['email']
        update_object.description=request.POST['description']
        update_object.save()

        messages.success(request, "Your profile was updated")

    return redirect('/users/edit')

def updatepw(request):
    if not request.session.get('logged_in'):
        return redirect('/')

    status, password_hash=User.objects.validate_update_pw(request)
    if status:
        update_object=User.objects.get(id=request.session['id'])
        update_object.pwh=password_hash
        update_object.save()
        messages.success(request, "Your password was updated")

    return redirect('/users/edit')

def dashboard(request):
    context = {
    'users' : User.objects.all(),
    }

    if request.session.get('logged_in'):
        if request.session['level']==9:
            return redirect('/dashboard/admin')
        return render(request, 'dashboard_app/dashboard.html', context)

    if User.objects.login(request):
        if request.session['level']==9:
            return redirect('/dashboard/admin')
        return render(request, 'dashboard_app/dashboard.html', context)
    else:
        return redirect('/login')

def show(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if User.objects.validate_id(request, id):
        context = {
        'user' : User.objects.get(id=id),
        'user_messages' : Message.objects.filter(recipient=id),
        'comments' : Comment.objects.filter(message__recipient=id),
        }
        return render(request, 'dashboard_app/showuser.html', context)
    else:
        return redirect('/dashboard')

def submit_message(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if User.objects.validate_id(request, id):
        recipient=User.objects.get(id=id)
        sender=User.objects.get(id=request.session['id'])
        Message.objects.create(message=request.POST['message'], sender=sender, recipient=recipient)

    return redirect('/users/show/'+str(id))

def submit_comment(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if User.objects.validate_id(request, id):
        if Message.objects.validate_message_id(request, request.POST['message_id']):
            message_object=Message.objects.get(id=request.POST['message_id'])
            sender=User.objects.get(id=request.session['id'])
            Comment.objects.create(comment=request.POST['comment'], message=message_object, sender=sender)

    return redirect('/users/show/'+str(id))

def update_admin(request, id):
    print "IN Admin update"
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.session['level'] != 9:
        messages.error(request, "You are not authorized to make this edit")
        return redirect('/dashboard')

    if User.objects.validate_update(request,id):
        update_object=User.objects.get(id=id)
        update_object.f_name=request.POST['f_name']
        update_object.l_name=request.POST['l_name']
        update_object.email=request.POST['email']
        update_object.description=request.POST['description']
        update_object.save()

        messages.success(request, "The user profile was updated")

    return redirect('/users/edit/'+str(id))

def updatepw_admin(request, id):
# Create your views here.
    print "IN Admin update"
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.session['level'] != 9:
        messages.error(request, "You are not authorized to make this edit")
        return redirect('/dashboard')
    status, password_hash=User.objects.validate_update_pw(request)
    if status:
        update_object=User.objects.get(id=id)
        update_object.pwd=password_hash
        update_object.save()
        messages.success(request, "Password updated, successfully")

    return redirect('/users/edit/'+str(id))

def confirm_delete(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.session['level'] != 9:
        messages.error(request, "You are not authorized for this operation!")
        return redirect('/dashboard')

    if User.objects.validate_id(request, id):
        delete_object=User.objects.get(id=id)
        if delete_object.level==9:
            messages.error(request, "You cannot delete the administrative account")
            return redirect('/dashboard')
        context = {
        'id' : id
        }
        return render(request, 'dashboard_app/confirm.html', context)

    return redirect('/dashboard')

def delete_user(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.session['level'] != 9:
        messages.error(request, "You are not authorized for this operation!")
        return redirect('/dashboard')
    if User.objects.validate_id(request, id):
        delete_object=User.objects.get(id=id)
        delete_object.delete()
        messages.success(request, "User object deleted!")

    return redirect('/dashboard')

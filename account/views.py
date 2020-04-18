from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Users, Followers
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
import os
import hashlib
import binascii
from chat.models import Room


# postgresql
def chat_key(key, *args):
    """Hash a password for storing."""
    password = key
    salt = hashlib.sha256(os.urandom(13)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def loginuser(request, user, userp):
    try:
        if request.session['user'] is None:
            print("error")
    except:
        request.session['user'] = user
        request.session["chat_key"] = chat_key(userp)
        print(request.session['user'])
    return request


def login(request):
    try:
        if request.session['user']:
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    except KeyError:
        pass

    def get_value(field_name):
        return request.POST.get(field_name)

    if request.method == 'POST':
        username = get_value('username')
        password = get_value('password')
        user = Users.objects.filter(username=username)
        try:
            user, userp, userisactive = user[0].username, user[0].password, user[0].status_is_active
            if userisactive == False:
                return render(request, 'account/login.html', {'notactive': True})
        except:
            print('here is the problem')
            return render(request, 'account/login.html', {'notvalid': True})
        if verify_password(userp, password):
            request = loginuser(request, user, userp)
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
        else:
            return render(request, 'account/login.html', {'notvalid': True})
    else:
        return render(request, 'account/login.html', {})


def logout(request):
    try:
        del request.session['user']
    except:
        print('error in logout')
    return render(request, 'account/login.html', {'loggedout': True})


def my_hash_function(password, *args):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def registration(request):
    try:
        if request.session['user']:
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    except KeyError:
        pass

    def get_value(field_name):
        return request.POST.get(field_name)

    if request.method == 'POST':
        username = get_value('username')
        first_name = get_value('first_name')
        last_name = get_value('last_name')
        date_of_birth = get_value('date_of_birth')
        job_title = get_value('job_title')
        department = get_value('department')
        email = get_value('email')
        contact = get_value('contact')
        password = my_hash_function(get_value('password1'), username)
        user = Users(username=username, slug=username, first_name=first_name, last_name=last_name,
                     date_of_birth=date_of_birth, job_title=job_title, department=department, email=email,
                     contact_number=contact, password=password)
        user.save()
        send_verification_mail(username, email)
        return render(request, 'account/login.html', {'registered': True})
    else:
        print("Here")
        return render(request, 'account/registration.html', {})


def verify_email(request, username):
    try:
        u = Users.objects.get(username=username)
        u.status_is_active = True
        u.save()
        return render(request, 'account/dashboard.html', {})
    except:
        print("invalid link has been processed")
        return HttpResponse("Invalid Url")


# from django.core.mail import send_mail
#
# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )
def send_verification_mail(username, email):
    EmailMessage(
        'Activation of your TalkChat Account',
        "Hello " + username + "! \n Below is the link to activate your TalkChat account. Visit 127.0.0.1:8000/account/verify/" + username + " so that you can continue using your account",
        to=[email, 'bindalmukul99@gmail.com']
    ).send()


def isUsernameAvaliable(request):
    username = request.GET.get("username")
    response = {
        "username_exists": "true"
    }
    if Users.objects.filter(username=username).__len__() > 0:
        return JsonResponse(response)
    else:
        response["username_exists"] = "false"
        return JsonResponse(response)


def hash_chat_id(user1, user2):
    key = 'asdASDFGHfgh0MNBVjklQWERTYqwU87O46512P3OIertyZuXioCpVzxBcvM9bnm'
    key_ = 'abcdefghijklmnopqrstuvwxyz0123465789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    chat_id = ''
    for x in str(user1):
        chat_id += key[key_.index(x)]
    for x in str(user2):
        chat_id += key[key_.index(x)]
    return chat_id


def hash_chat_key(id):
    key = 'asdASDFGHfgh0MNBVjklQWERTYqwU87O46512P3OIertyZuXioCpVzxBcvM9bnm'
    key_ = 'abcdefghijklmnopqrstuvwxyz0123465789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    chat_id = ''
    for x in str(id):
        chat_id += key[key_.index(x)]
    # for x in str(user2):
    # 	chat_id+= key[key_.index(x)]
    return chat_id


def follow(request):
    try:
        if request.session['user'] is None:
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    except KeyError:
        return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    if request.method == "POST":
        user1 = request.session['user']
        user2 = request.POST.get("username")
        user1 = Users.objects.filter(username=user1)
        user2 = Users.objects.filter(username=user2)
        chat_id1 = hash_chat_id(user1[0], user2[0])
        chat_id2 = hash_chat_id(user2[0], user1[0])
        does_exist1 = Room.objects.filter(name=chat_id1)
        if does_exist1.__len__() > 0:
            chat_id = chat_id1
        else:
            does_exist2 = Room.objects.filter(name=chat_id2)
            if does_exist2.__len__() > 0:
                chat_id = chat_id2
            else:
                chat_id = chat_id1

        try:
            follow = Followers(user1=user1[0], user2=user2[0], chat_id=chat_id)
            follow.save()
        except:
            pass
        try:
            room = Room(name=chat_id, description="Say Hi to you buddy", slug=chat_id)
            room.save()
        except:
            pass
    all_users = [x.username for x in Users.objects.exclude(username=request.session['user'])]
    return render(request, 'account/users.html', {'all_users': all_users})


def friends(request):
    try:
        if request.session['user'] is None:
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    except KeyError:
        return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    user = request.session['user']
    user = Users.objects.filter(username=user)[0]
    friends = Followers.objects.filter(user1=user)
    friends2 = Followers.objects.filter(user2=user)
    list_of_friends = [(x.user2, x.chat_id) for x in friends] + [(x.user1, x.chat_id) for x in friends2]
    return render(request, 'account/friends.html', {'list_of_friends': list_of_friends})


def getchatkey(request):
    response = {
    }
    try:
        if request.session['user'] is None:
            return JsonResponse(response)
    except KeyError:
        return JsonResponse(response)
    chat_key = hash_chat_key(request.GET.get('chat_id'))
    while len(chat_key) < 16:
        chat_key *= 2
    print("chat key is ", chat_key[0:16])
    response["chat_key"] = chat_key[0:16]
    return JsonResponse(response)

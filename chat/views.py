from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
# from faker import Faker
# from twilio.jwt.access_token import AccessToken
# from twilio.jwt.access_token.grants import ChatGrant
from .models import Room , ReadMessages , UnreadMessages
from account.models import Followers,Users
from . import spam_detection
from Crypto.Cipher import AES
#fake = Faker()


def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    user = Followers.objects.get(chat_id = slug)
    if request.session['user'] in [user.user1.username , user.user2.username]:
        receiver = user.user1.username if request.session['user']!=user.user1.username else user.user2.username
        data = {'room': room,'sender':request.session['user'],'receiver':receiver , 'chat_id':slug}
        return render(request, 'chat/chat.html', data)
    else:
        return JsonResponse({"access":"denied"})

# This function will be called by twilio javascript in order to get a unique 
# token so that any end-user can use the chat service using my twilio api-key and 
# account-sid. In Javascript , this funtion will return a json response containing 
# unique token.
# def token(request):
#     # using below two variables to create a unique identifier of a user-end
#     # each user's device-id + his username is always a unique combination
#     identity = request.GET.get('identity', request.session['user'])
#     device_id = request.GET.get('device', 'default')  # unique device ID
    
#     # Below lines just fetch authentication keys from settings
#     account_sid = settings.TWILIO_ACCOUNT_SID
#     api_key = settings.TWILIO_API_KEY
#     api_secret = settings.TWILIO_API_SECRET
#     chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID
    
    
#     # generate a unique access-token. Identity arguement is used for uniqueness
#     # for each individual user.
#     token = AccessToken(account_sid, api_key, api_secret, identity=identity)


#     # Create a unique endpoint ID for the device
#     endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

#     # finally grant chat permission.
#     if chat_service_sid:
#         chat_grant = ChatGrant(endpoint_id=endpoint,
#                                service_sid=chat_service_sid)
#         token.add_grant(chat_grant)

#     response = {
#         'identity': identity,
#         'token': token.to_jwt().decode('utf-8')
#     }
    
#     return JsonResponse(response)
def tokenn(request):
    msg = request.GET.get('message')
    print(msg)
    response = {
        'messagefrompython':msg
    }
    
    return JsonResponse(response)
def receivemsg(request):
    chat_id = Followers.objects.filter(chat_id = request.GET.get('chat_id'))
    try:
        if request.session['user'] is None or (request.GET.get('From') not in [chat_id[0].user1.username , chat_id[0].user2.username]):
            return render(request,'account/dashboard.html',{'section':'dashboard'})
    except KeyError:
        return render(request,'account/dashboard.html',{'section':'dashboard'})
    #chat_id = Followers.objects.filter(chat_id = request.GET.get('chat_id'))
    From = Users.objects.filter(username = request.GET.get('From'))
    To = Users.objects.filter(username = request.GET.get('To'))
    message = request.GET.get('message')

    row = UnreadMessages(chat_id = chat_id[0] , From = From[0] , To = To[0] , message = message)
    row.save()
    response = {'status':"success" , "message_from_python":message,"time" : str(timezone.now)}
    return JsonResponse(response)

def sendmsg(request):
    chat_id = Followers.objects.filter(chat_id = request.GET.get('chat_id'))
    
    From = Users.objects.filter(username = request.GET.get('From'))
    To = Users.objects.filter(username = request.GET.get('To'))
    messages = UnreadMessages.objects.filter(chat_id = chat_id[0] , From = From[0] , To = To[0])
    response = {
        'status':'success',
        "messages" : [],
        "length" : 0
    }
    for msg in messages:
        response["messages"].append(msg.message)
        ReadMessages(chat_id = msg.chat_id , From = msg.From , To = msg.To , message = msg.message).save()
    response["length"] = response["messages"].__len__()
    messages.delete()
    #print(response)
    return JsonResponse(response)

def readmsg(request):
    chat_id = Followers.objects.filter(chat_id = request.GET.get('chat_id'))
    messages = ReadMessages.objects.filter(chat_id = chat_id[0]).order_by('time_date')
    messages = messages[max(0 , len(messages)-30):]
    response = {
        'status':'success',
        "messages" : [],
        "length" : 0
    }
    for msg in messages:
        response["messages"].append({"from":msg.From.username ,"message":msg.message})
    response["length"] = response["messages"].__len__()
    return JsonResponse(response)




def checkspam(request):
    message = request.GET.get('message')
    status = (spam_detection.is_spam(message))
    print(status)
    return JsonResponse({'status':status})

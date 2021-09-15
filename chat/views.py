from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from asgiref.sync import sync_to_async
from tortoise import Tortoise
from django.conf import settings
from django.views.generic import View
from django.db.models import Min

from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode
from datetime import datetime
from datetime import date
from datetime import datetime
from datetime import date
from django.contrib import messages
from .forms import NewReportForm

# Create your views here.

# chat/views.py
from django.shortcuts import render
from .models import ChatGroup
from .tortoise_models import ChatMessage

# index page of chat
@login_required
def index(request):
    assigned_groups = list(request.user.groups.values_list('id', flat=True))
    groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)
    group_id = min(assigned_groups)
    chatgroup = ChatGroup.objects.get(id=group_id)

    return render(request, 'chat/index.html', {
        'chatgroup': assigned_groups[0],
        'groups_participated': groups_participated
    })

def get_participants(group_id=None, group_obj=None, user=None):
    """ function to get all participants that belong the specific group """

    if group_id:
        chatgroup = ChatGroup.objects.get(id=id)
    else:
        chatgroup = group_obj

    temp_participants = []
    for participants in chatgroup.user_set.values_list('username', flat=True):
        if participants != user:
            temp_participants.append(participants.title())
    temp_participants.append('You')
    return ', '.join(temp_participants)

# room interface
@login_required
def room(request, group_id):

    if request.user.groups.filter(id=group_id).exists():
        chatgroup = ChatGroup.objects.get(id=group_id)
        #TODO: make sure user assigned to existing group
        assigned_groups = list(request.user.groups.values_list('id', flat=True))
        groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)
        return render(request, 'chat/room.html', {
            'chatgroup': chatgroup,
            'participants': get_participants(group_obj=chatgroup, user=request.user.username),
            'groups_participated': groups_participated
        })

    else:
        return HttpResponseRedirect(reverse("chat:unauthorized"))

# send unauthorised for wrong room
@login_required
def unauthorized(request):
    return render(request, 'chat/unauthorized.html', {})

# get chat history
async def history(request, room_id):

    await Tortoise.init(**settings.TORTOISE_ORM)
    chat_message = await ChatMessage.filter(room_id=room_id).order_by('date_created').values()
    await Tortoise.close_connections()

    return await sync_to_async(JsonResponse)(chat_message, safe=False)

# ajax call to decrypt messages
def get(request):
    if request.is_ajax():
        message = request.GET.get('message')
        nonce = request.GET.get('nonce')
        key = b'\xa8|Bc\xf8\xba\xac\xca\xdc/5U0\xe3\xd6f'
        cipher = AES.new(key, AES.MODE_CTR)
        nonce_ = nonce
        msg_ = message
        key = key
        nonce = b64decode(nonce_)
        ct = b64decode(msg_)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        msg_ = cipher.decrypt(ct)
        message = msg_.decode()

        return JsonResponse({'message': message})

    return render(request, 'chat/room.html')

# help page
@login_required
def help(request):
    return render(request, 'chat/help.html', {})

# reporting interface
@login_required
def report(request):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    today = date.today()
    form = NewReportForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Report was successful." )
        return redirect("chat:report")
    messages.error(request, "Unsuccessful reporting. Invalid information.")
    return render(request, 'chat/report.html', {'time':time,'date':today,'form':form})

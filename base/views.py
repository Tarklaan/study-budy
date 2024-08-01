from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import FormRoom,UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        else:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Username or password is incorrect')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context={'form':form}
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error occured')
    return render(request,'base/login_register.html',context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()[0:5]  # type: ignore
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    room_count = rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,"base/home.html",context)

def room(request,pk):
    r=Room.objects.get(id=pk)
    roomMessages = r.message_set.all().order_by('-created') # type: ignore
    participants = r.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=r,
            body=request.POST.get('body')
        )
        r.participants.add(request.user)
        return redirect('room',pk=r.id) # type: ignore
    context={'rooms':r,'roomMessages':roomMessages,'participants':participants}
    return render(request,"base/room.html",context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all() # type: ignore
    roomMessages =user.message_set.all().order_by('-created') # type: ignore
    topics= Topic.objects.all()
    context={'user':user,'rooms':rooms,'roomMessages':roomMessages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def Create_Room(request):
    f=FormRoom()
    topics=Topic.objects.all()
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # f=FormRoom(request.POST)
        # if f.is_valid():
        #     room=f.save(commit=False)
        #     room.host = request.user
        #     room.save() 
        return redirect('/')
    
    context={"form":f,'topics':topics}
    return render(request,"base/form_room.html",context)

@login_required(login_url='/login')
def Update_Room(request,pk):
    room = Room.objects.get(id=pk)
    topics=Topic.objects.all()
    f=FormRoom(instance=room)
    if request.user != room.host:
        return HttpResponse('Your are not allowed to do that princess!!')
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        f=FormRoom(request.POST)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        # if f.is_valid():
        #     f.save() 
        return redirect('/')
    context={"form":f,'topics':topics,'rooms':room}
    return render(request,"base/form_room.html",context)

@login_required(login_url='/login')
def delete(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed to do that princess!!')
    if request.method == "POST":
        room.delete()
        return redirect("/")
    return render(request,"base/delete.html",{'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed to do that princess!!')
    if request.method == "POST":
        message.delete()
        return redirect("/")
    return render(request,"base/delete.html",{'obj':message})

@login_required(login_url='/login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=="POST":
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request,'base/update-user.html',{'form':form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activity(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
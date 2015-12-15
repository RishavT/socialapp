from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def newsfeed(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    user = request.user
    if 'owner' not in request.GET.dict().keys():
        owner = user.customuser
    else:
        owner = CustomUser.objects.filter(pk=int(request.GET['owner'])).first()
    if not owner:
        return HttpResponse('404 not found')
    statuses = owner.statuses.all()
    return render(request, 'newsfeed.html', {'statuses':statuses, 'owner':owner})

@csrf_exempt
def status(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    user = request.user
    
    if request.method=='POST':
        form = StatusForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = request.POST['data']
            status = Status(data=data,owner=user.customuser)
            status.save()
            return HttpResponseRedirect('/newsfeed')
    
    if 'status_id' not in request.GET.dict().keys():
        form = StatusForm()
        return render(request, 'statusform.html', {'form': form})
        
    status = Status.objects.get(pk=int(request.GET['status_id']))
    if not status:
        return HttpResponse('404 Not found')
    likes = status.likes.filter(up=True).count()
    dislikes = status.likes.filter(up=False).count()
    return render(request, 'status.html', {'status':status,
                                            'comments':status.comments.all(),
                                            'likes':likes,
                                            'dislikes':dislikes,})

@csrf_exempt
def profile(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    user = request.user
    me = True
    if 'id' not in request.GET.dict().keys() or int(request.GET['id']) != user.pk:
        me = False
    return render(request, 'profile.html', {'user':user, 'me':me})

def logout_do(request):
    logout(request)
    return HttpResponseRedirect('/login')

@csrf_exempt
def login_do(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if not user:
                return HttpResponse('login failed')
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/newsfeed?user=%s' % user.username)
            else:
                return HttpResponse('User deactivated.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
    
    


####Form views
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            if password != request.POST['password2']:
                return HttpResponse('Passwords do not match')
            user = User.objects.create_user(username=username, password=password)
            
            user.save()
            customuser = CustomUser(user=user)
            customuser.save()
            return HttpResponseRedirect('/login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})

def comment(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    if request.method == 'POST':
        if 'id' not in request.GET.dict().keys():
            return HttpResponse('404 not found')
        status = Status.objects.get(pk=int(request.GET['id']))
        if not status:
            return HttpResponse('404x not found')
        if 'data' not in request.POST.dict().keys():
            return HttpResponse('Invalid request')
        comment = Comment(data=request.POST['data'],status=status,owner=request.user.customuser)
        comment.save()
        return HttpResponseRedirect('/status?status_id=' + str(status.pk))
    else:
        if 'id' not in request.GET.dict().keys():
            return HttpResponse('404 not found')
        status = Status.objects.get(pk=int(request.GET['id']))
        form = CommentForm()
    return render(request, 'comment.html', {'form':form, 'status':status})

def like_status(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    user = request.user
    if request.method == 'GET':
        if 'id' not in request.GET.dict().keys():
            return HttpResponse('404 not found')
        status =  Status.objects.get(pk=int(request.GET['id']))
        if not status:
            return HttpResponse('404 not found')
        like = StatusLike.objects.filter(parent=status).first()
        if not like:
            like = StatusLike(parent=status,up=True,owner=user.customuser)
        if 'negative' in request.GET.dict().keys():
            if request.GET['negative'] == '1':
                like.up=False
        if 'positive' in request.GET.dict().keys():
            if request.GET['positive'] == '1':
                like.up=True
        like.save()
        return HttpResponseRedirect('/status?status_id=' + str(status.pk))
    return HttpResponse('Invalid request')

def search(request):
    if request.user:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    user = request.user
    if request.method == 'GET':
        if 'username' not in request.GET.dict().keys():
            return HttpResponse('404 not found')
        #return HttpResponse(request.GET['username'])
        customuser = User.objects.get(username=request.GET['username'])
        #return HttpResponse(customuser.username)
        if customuser:
            #return HttpResponse(request.GET['username'])
            return HttpResponseRedirect('/newsfeed?owner=' + str(customuser.customuser.pk))
        else:
            return HttpResponse('404 not found')
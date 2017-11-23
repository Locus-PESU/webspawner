from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.files import File
from django.http import HttpResponse
from .models import RootProfile
from forum.models import Forum, Board, Category
import datetime


def index(request):
    if request.user.is_authenticated:
        profile = RootProfile.objects.get(user=request.user)
        items = profile.forums.all()
        if not items:
            no_items = '(You haven\'t created any websites yet.)'
        else:
            no_items = ''
        ctx = {
            'no_items': no_items,
            'forums': profile.forums.all(),
            'all_forums': Forum.objects.exclude(owner=request.user.rootprofile)
        }
        return render(request, 'mainapp/dashboard.html', ctx)

    return redirect('/guestpage/')


def guestpage(request):
    return render(
        request, 'mainapp/guestpage.html',
        {'forums': Forum.objects.all()})


def signup_view(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request method')
    if User.objects.filter(username=request.POST['username']):
        return render(
            request, 'mainapp/guestpage.html',
            {
                'availability': 'Username already exists',
                'forums': Forum.objects.all()})
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email']
    )
    fl = request.FILES.get('user_dp', False)
    if not fl:
        prof = RootProfile(user=user, quote=request.POST.get('quote', ''))
        prof.avatar.save(
            request.POST['username']+'.jpg',
            File(open('Anonymous_User.jpg', 'rb'))
        )

    else:
        prof = RootProfile(user=user)
        # f = open(request.POST['username']+'.jpg', 'wb')
        # f.write(request.FILES['user_dp'].read())
        # f.close()
        prof.avatar.save(
            request.POST['username']+'.jpg',
            request.FILES['user_dp']
        )

    login(request, user)
    return redirect('/')


def login_view(request):
    if request.method == 'GET':
        return redirect('/')
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        return render(
            request, 'mainapp/guestpage.html',
            {
                'auth_validity': 'Invalid credentials',
                'forums': Forum.objects.all()})
    login(request, user)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def new_forum(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        ctx = {'n_boards': range(3), 'n_subboards': range(3)}
        return render(request, 'mainapp/new_forum.html', ctx)
    forum = Forum.objects.filter(name=request.POST['name'])
    if forum:
        return render(
            request, 'mainapp/new_forum.html',
            {
                'already_exists': 'Forum with that name already exists',
                'n_boards': range(3), 'n_subboards': range(3)})
    profile = RootProfile.objects.get(user=request.user)
    forum = Forum.objects.create(
        owner=profile,
        name=request.POST['name'],
        punchline=request.POST.get('punchline', ''),
        description=request.POST.get('description', ''),
        url=request.POST['name'].replace(' ', '_'),
        created_on=datetime.datetime.now()
    )
    if request.FILES.get('cover', False):
        forum.thumb.save(request.POST['name']+'.jpg', request.FILES['cover'])
    else:
        forum.thumb.save(
            request.POST['name']+'.jpg',
            File(open('vangogh_field.jpg', 'rb'))
        )
    if request.FILES.get('bg', False):
        forum.bg.save(request.POST['name']+'_bg.jpg', request.FILES['bg'])
    else:
        forum.bg.save(
            request.POST['name']+'_bg.jpg',
            File(open('boris.jpg', 'rb'))
        )
    if request.FILES.get('bg_thread', False):
        forum.bg_thread.save(
            request.POST['name']+'_thread.jpg', request.FILES['bg_thread'])
    else:
        forum.bg_thread.save(
            request.POST['name']+'_thread.jpg',
            File(open('gothic_lab.png', 'rb'))
        )
    for i in range(3):
        if not request.POST.get('board' + str(i)):
            break
        cat = Category.objects.create(
            forum=forum,
            name=request.POST['board' + str(i)],
            created_on=datetime.datetime.now(),
            description=request.POST.get('board_desc', None)
        )
        for j in range(3):
            if not request.POST.get('sb' + str(i) + '_' + str(j)):
                break
            Board.objects.create(
                category=cat,
                name=request.POST['sb' + str(i) + '_' + str(j)],
                created_on=datetime.datetime.now()
            )
    return redirect('/forum/' + forum.url + '/')


def profile_settings(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'mainapp/profile_settings.html')
    if request.POST.get('password', False):
        request.user.set_password(request.POST['password'])
        request.user.save()
    if request.FILES.get('dp', False):
        prof = RootProfile.objects.get(user=request.user)
        prof.avatar.save(request.user.username+'.jpg', request.FILES['dp'])
    if request.POST.get('quote', False):
        prof = RootProfile.objects.get(user=request.user)
        prof.quote = request.POST['quote']
        prof.save()
    return redirect('/')

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
# from homeapp.utils import visit_count, trimmed_visit_count
from .models import Category, Board, Thread, User, Post, Forum
from .forms import AddThread, AddPost
from collections import OrderedDict
import datetime


def index(request, furl):
    context = {}
    if not request.user.is_authenticated:
        context['login_button'] = 'Log In'
        context['member'] = 'Guest'
    else:
        context['login_button'] = 'Log Out'
        context['member'] = request.user.username
    categs = Category.objects.filter(forum__url=furl)
    print(furl)
    categ_dict = OrderedDict()
    for categ in categs:
        categ_dict[categ.name] = categ.board_set.all().order_by(
            '-last_thread_on')
    context['categs'] = categ_dict
    context['forum'] = Forum.objects.get(url=furl)
    return render(request, 'forum/index.html', context)


def board(request, board_id, page):
    page = int(page)
    context = {}
    board = Board.objects.filter(pk=board_id)
    if not board:
        return HttpResponse('Board does not exist')
    board = board[0]
    if page == 1:
        pinneds = board.thread_set.filter(thread_type='PN')
        anns = board.thread_set.filter(thread_type='AM')
        threads = board.thread_set.filter(
            thread_type='NM').order_by('-started_on')[:30]
        context['pinneds'] = pinneds
        context['anns'] = anns
        context['threads'] = threads
    else:
        threads = board.thread_set.filter(
            thread_type='NM').order_by(
            '-started_on')[(page-1)*30:30+(page-1)*30]
        if not threads:
            return HttpResponse('No more threads to display')
        context['threads'] = threads
    context['title'] = board.name
    context['board_id'] = board.id
    context['forum'] = board.category.forum
    return render(request, 'forum/board.html', context)


def thread(request, thread_id, page):
    page = int(page)
    context = {}
    thread = Thread.objects.filter(pk=thread_id)
    if not thread_id:
        raise Http404('The thread doesn\'t exist')
    thread = thread[0]
    posts = thread.post_set.all()[(page-1)*30:30+(page-1)*30]
    if not posts:
        return HttpResponse('No more posts to display')
    context['forum'] = thread.board.category.forum
    context['posts'] = posts
    context['thread'] = thread
    context['id'] = thread_id
    context['form'] = AddPost()
    return render(request, 'forum/thread.html', context)


def add_thread(request, board_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    board = Board.objects.get(pk=board_id)
    b_name = board.name
    return render(
        request, 'forum/add_thread.html',
        {'id': board_id, 'board': b_name})


def add_post(request, thread_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    form = AddPost()
    return render(
        request, 'forum/add_post.html', {'form': form, 'id': thread_id})


def display_user(request, user_id, page):
    page = int(page)
    context = {}
    user = User.objects.filter(pk=user_id)
    if not user:
        raise Http404('User does not exist')
    user = user[0]
    context['user'] = user
    posts = user.post_set.all()[(page-1)*30:30+(page-1)*30]
    context['posts'] = posts
    if not bool(user.dp):
        dp_url = None
    else:
        dp_url = user.dp.url
    context['dp_url'] = dp_url
    return render(request, 'forum/display_user.html', context)


def upload_new_thread(request, board_id):
    # handle parsing the form fields and processing it
    # award 10 karma to the uploader
    if not request.user.is_authenticated:
        return redirect('/login/')
    form = AddThread(request.POST)
    if form.is_valid():
        present = datetime.datetime.now()
        board = Board.objects.get(pk=board_id)
        thread = Thread(
            board=board,
            title=form.cleaned_data['title'],
            thread_type=form.cleaned_data['type_'],
            creator=request.user,
            started_on=present,
            last_post_on=present,
            last_post_by=request.user
        )
        thread.save()
        post = Post(
            thread=thread,
            author=request.user,
            content=form.cleaned_data['post'],
            post_time=present
        )
        post.save()
        board.last_thread_on = present
        board.save()
    else:
        return HttpResponse('Invalid form')
    return redirect('/forum/board/'+str(board_id)+'/1/')


def upload_new_post(request, thread_id):
    # handle the form and process it
    # award 10 karma to the uploader
    if not request.user.is_authenticated:
        return redirect('/login/')
    form = AddPost(request.POST)
    if form.is_valid():
        thread = Thread.objects.get(pk=thread_id)
        present = datetime.datetime.now()
        post = Post(
            thread=thread,
            author=request.user,
            content=form.cleaned_data['content'],
            post_time=present
        )
        post.save()
        thread.last_post_on = present
        thread.last_post_by = request.user
        thread.post_count += 1
        thread.save()
    else:
        return HttpResponse('Invalid form')
    return redirect('/forum/thread/'+str(thread_id)+'/1/')


def add_rating(request, post_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    post = Post.objects.filter(pk=post_id)
    if not post:
        raise Http404('Post not found')
    post = post[0]
    rated = post.rating_set.filter(rater=request.user)
    if rated:
        return HttpResponse('Already rated this post')
    post.rating_set.create(
        rater=request.user,
        rating_point=request.POST['rating_point']
    )
    return HttpResponse('Rating added')


def send_dm(request, user_id):
    return HttpResponse('Feature coming soon')


def search(request):
    return HttpResponse('Feature coming soon')

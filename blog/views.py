import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from blog.forms import PostForm, LoginForm
from blog.models import Post


def index(request):
    return render(request, 'blog/index.html')


class LoginView(View):
    def get(self, request):
        return render(request, "blog/login_page.html", {"login_form": LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("posts"))
        return render(request, "blog/login_page.html", {"login_form": form})


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('login'))

    context = {'form': form}
    return render(request, 'blog/register.html', context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def posts(request):
    posts = Post.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blog/posts.html', context)


@login_required
def sort_posts_from_old_to_new(request):
    posts = Post.objects.order_by('date_added')
    return render(request, 'blog/posts.html', {'posts': posts})


@login_required
def sort_posts_from_new_to_old(request):
    posts = Post.objects.order_by('-date_added')
    return render(request, 'blog/posts.html', {'posts': posts})


@login_required
def sort_posts_from_last_24_hours(request):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    posts = Post.objects.filter(
        date_added=date_from).order_by('-date_added')
    return render(request, 'blog/posts.html', {'posts': posts})


@login_required
def current_user_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'blog/posts.html', {'posts': posts})


@login_required
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('posts'))

    context = {'form': form}
    return render(request, 'blog/new_post.html', context)

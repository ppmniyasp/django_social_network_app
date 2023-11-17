from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import transaction

from post.models import Post, Tag, Follow, Stream, Likes, Comment
from .forms import NewPostform, NewCommentForm
from django.contrib.auth.models import User
from users.models import Profile
from .utils import searchProfile



# Create your views here.
@login_required(login_url="login")
def index(request):
    user = request.user
    user_post = Post.objects.filter(user=user)
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=user)
    likes = Likes.objects.filter(user=user)

    profile = Profile.objects.all()
    search_profile, search_query = searchProfile(request)

    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in user_post:
        group_ids.append(post.id)

    for post in posts:
        group_ids.append(post.post_id)
    print(group_ids)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'search_profile': search_profile,
        'search_query': search_query,
        'likes' : likes
        # 'users_paginator': users_paginator,
    }
    return render(request,'index.html', context)


def new_post(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'post/new_post.html', context)

def post_details(request, pk):
    user = request.user
    post = get_object_or_404(Post, id = pk)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid:
            cmnt = form.save(commit=False)
            cmnt.user = user
            cmnt.post = post
            cmnt.save()
            return redirect("post-details", pk)
    else:
        form = NewCommentForm()


    context ={
        'post' : post,
        'form' : form,
        'comments': comments
    }
    return render(request, 'post/post_details.html',context)

def tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = tag.tags.all().order_by('-posted')

    context = {
        'tag' : tag,
        'posts' : posts
    }
    return render(request, 'post/tag.html', context)


def like(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    print(liked)

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes  += 1
        print('"liked"')
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
        print('"un liked"')

    post.likes = current_likes
    post.save()

    return redirect("post-details", pk)

def favourite(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=pk).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[pk]))

def follow(request, username, option):
    user = request.user
    following_user = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following_user)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following_user, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following_user)
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following_user)
                    stream.save()
        return redirect('profile', username)
    except User.DoesNotExist:
        return redirect('profile', username)

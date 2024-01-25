from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Notification
from .forms import NewPostForm, UpdatePostForm, CommentForm


def home(request):
    posts = Post.objects.all()

    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # return redirect("blog:detail", pk=post.id)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/post_detail.html", context)


@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:home")
    else:
        form = NewPostForm()
    context = {
        "form": form,
        "title": "Create Post"
    }
    return render(request, "blog/form.html", context)


@login_required
def update_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.user != post.author:
        return redirect("blog:detail", pk=post.id)

    if request.method == "POST":
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:detail", pk=post.id)
    else:
        form = UpdatePostForm(instance=post)
    context = {
        "form": form,
        "post": post,
        "title": "Update Post"
    }
    return render(request, "blog/form.html", context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, created_by=request.user)

    if request.user != post.author:
        return redirect("blog:home")

    if request.method == "POST":
        post.delete()
        return redirect("blog:home")

    context = {
        "post": post,
    }
    return render(request, "blog/post_delete.html", context)


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    context = {
        "posts": user_posts,
    }
    return render(request, "blog/dashboard.html", context)


def one_user_post(request, username):
    post_author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=post_author)
    post_count = posts.count()
    context = {
        "posts": posts,
        "post_author": post_author,
        "post_count": post_count,
    }
    return render(request, "blog/user_post.html", context)


# Notification view
@login_required
def notifications(request):
    user = request.user
    user_notifications = Notification.objects.filter(user=user, is_read=False)

    context = {
        "user_notifications": user_notifications,
    }
    return render(request, "blog/notifications.html", context)

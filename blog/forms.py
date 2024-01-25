from django import forms

from .models import Post, Comment


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


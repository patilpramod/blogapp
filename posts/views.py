from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Post
from .forms import PostForm


# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'post_form.html', context)

def post_detail(request,id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, 'post_details.html', context)

def post_list(request):
    qs = Post.objects.all()
    context = {
        "title": "Yes",
        "object_list" : qs
    }
    return render(request, 'base.html', context)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, 'post_form.html', context)

def post_delete(request,id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect('list')
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# Create your views here.

def post_create(request):
    context = {
        "title": "Create"
    }
    return render(request, 'index.html', context)

def post_detail(request,id=None):
    instance = get_object_or_404(Post,id=id)
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
    return render(request, 'index.html', context)

def post_update(request):
    return HttpResponse("<h1> uda</h1>")

def post_delete(request):
    return HttpResponse("<h1> Hdel</h1>")
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from urllib.parse import quote_plus
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'post_form.html', context)

def post_detail(request,slug_id=None):
    instance = get_object_or_404(Post,  slug=slug_id)
    if instance.draft : #or instance.publish >= timezone.now().date:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content, safe='', encoding=None, errors=None)# urlparse(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string" : share_string,
    }
    return render(request, 'post_details.html', context)

def post_list(request):
    today = timezone.now().date()
    if request.user.is_staff or request.user.is_superuser:
        qs = Post.objects.all().order_by('-timestamp')
    else:
        qs = Post.objects.active().order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
       #     Q(user__name__icontains=query) #|
            Q(user__first_name__icontains=query) |
           Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(qs, 5)
    page_request_var = 'pageindex'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)
    context = {
        "title": "Blogs",
        "object_list" : page_obj,
        "page_request_var" : page_request_var,
        'today' : today
    }
    return render(request, 'post_list.html', context)

def post_update(request, slug_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug_id)
    form = PostForm(request.POST or None, request.FILES or None , instance=instance,  )
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

def post_delete(request,slug_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,  slug=slug_id)
    instance.delete()
    return redirect('list')
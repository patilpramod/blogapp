from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
# Create your models here.

class PostManager(models.Manager):

    ## Returns all the posts which are not in draft state and publish date is less than or equal to current time
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    return ''.format(instance.pk, filename)


class Post(models.Model):
    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title     = models.CharField(max_length=120)
    slug      = models.SlugField(unique=True)
    draft     = models.BooleanField(default=False)
    publish   = models.DateField(auto_now_add=False,auto_now=False)
    image     = models.ImageField(upload_to=upload_location,
                                  null=True,blank=True,
                                  width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated   = models.DateTimeField(auto_now=True,auto_now_add=False)

    objects = PostManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/posts/{self.slug}/'

    class Meta:
        ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


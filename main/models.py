from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, update_last_login
from django.db.models.signals import post_save
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=80, null=True,  blank=True)
    bio = models.TextField(max_length=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='users', blank=True, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)
    thumbnil = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name


# class Following(models.Model):
#     follow = models.ForeignKey(Category, on_delete=models.CASCADE)
#     add_follow = models.IntegerField(default=0)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    thumbnil = models.ImageField(upload_to='post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = RichTextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('published_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    follow_count = models.IntegerField(default=0)


class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=300, null=True)


class Questions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CONDITION_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('anonymous', 'Anonynomous')
    ]
    question_title=models.TextField(max_length=200)
    question_link=models.URLField(max_length=200)
    optional_content = models.TextField(max_length=200)
    optional_link= models.URLField(max_length=200)





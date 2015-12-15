from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

class Status(models.Model):
    data = models.TextField()
    date_created = models.DateTimeField(auto_now=False,auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    owner = models.ForeignKey(CustomUser, related_name='statuses')
    def __unicode__(self):
        return self.data

class Comment(models.Model):
    data = models.TextField()
    date_created = models.DateTimeField(auto_now=False,auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    status = models.ForeignKey(Status, related_name='comments')
    owner = models.ForeignKey(CustomUser, related_name='comments')
    def __unicode__(self):
        return self.data

class CommentLike(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='commentlikes')
    up = models.BooleanField()
    parent = models.ForeignKey(Comment, related_name='likes')
class StatusLike(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='statuslikes')
    up = models.BooleanField()
    parent = models.ForeignKey(Status, related_name='likes')
    
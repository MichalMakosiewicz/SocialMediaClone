from django.db import models
from django.urls import reverse
from django.conf import settings
from django.forms import ModelForm

import misaka

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Post(ModelForm):
    user =  models.ForeignKey(User,related_name='post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='post', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)

    def get_absolute_url(self):
        return reverse('post:single',kwargs={'username':self.user.username,
                                            'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        allow_unicode = ['user','message']

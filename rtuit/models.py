from datetime import datetime 
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse
from django.db import models

class Trend(Document):
    query = StringField(max_length=200, required=False)
    name = StringField(required=True)
    url = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.now)
    is_published = BooleanField(default=True)


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Trend, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    def get_edit_url(self):
        return reverse('update', args=[self.id])

    def get_delete_url(self):
        return reverse('delete', args=[self.id])


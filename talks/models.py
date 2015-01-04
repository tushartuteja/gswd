from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class TalkList(models.Model):
    user = models.ForeignKey(User,related_name='lists')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=355, blank=True)

    class Meta():
        unique_together = ('user', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TalkList, self).save(*args, **kwargs)

    def get_absolute_url(self):
         return reverse('talks:lists:detail', kwargs={'slug': self.slug})



class Talk(models.Model):
    ROOM_CHOICES = (
        ('517D', '517D'),
        ('517C', '517C'),
        ('517AB', '517AB')
    )
    talk_list = models.ForeignKey(TalkList, related_name='talks')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    when = models.DateTimeField()
    room = models.CharField(max_length=5, choices=ROOM_CHOICES)
    host = models.CharField(max_length=255)

    class Meta:
        ordering = ('when', 'room')
        unique_together = ('talk_list', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Talk, self).save(*args, **kwargs)





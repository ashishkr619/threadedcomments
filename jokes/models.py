from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from comments.models import Comment


class Joke(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='jokes')
    content = models.CharField(max_length=255)
    # slug = models.SlugField(unique=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('jokes_detail',args=[self.pk])  

    @property
    def comments(self):
        instance=self
        qs= Comment.objects.filter_comments_by_joke(instance)
        return qs    

    @property #get the content type for our particular model
    def get_content_type(self):
        instance=self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type





        


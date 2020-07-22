from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class CommentManager(models.Manager):

    def all(self):
        qs= super(CommentManager,self).filter(parent=None)
        return qs

    def filter_comments_by_joke(self,instance):
        # content_type = ContentType.objects.get_for_model(Joke)
        content_type = ContentType.objects.get_for_model(instance.__class__)#another way of saying the above thing
        obj_id = instance.id
        qs = super().filter(content_type=content_type,object_id = obj_id)#pass additional context
        return qs


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    content = models.CharField(max_length=255)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects= CommentManager()

    class Meta:
        ordering=['-timestamp']


    def __str__(self):
        return self.content

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True    


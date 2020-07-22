from django.forms import ModelForm
from django import forms
from comments.models import Comment


class CommentForm(ModelForm):
    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label='', widget=forms.Textarea)

    class Meta:
        model =Comment
        fields=['content',]
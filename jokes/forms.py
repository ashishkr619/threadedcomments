from django.forms import ModelForm
from jokes.models import Joke


class JokeForm(ModelForm):

    class Meta:
        model= Joke
        fields =['content']

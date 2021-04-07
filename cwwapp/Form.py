from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('headline', 'region','details','category')

        error_messages = {
            'headline':{'required':"is empty, please enter something",},
            'region':{'required':"is empty, please enter something",},
            'details':{'required':"is empty, please enter something",},
            'category':{'required':"is empty, please enter something",}
        }

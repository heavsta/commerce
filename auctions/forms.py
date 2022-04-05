from typing import Text
from django import forms
from django.forms.widgets import Textarea

from auctions.models import Category

class ListingForm(forms.Form):
    title = forms.CharField(label='', max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Category', label='')
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Short Description of the Product'}), label='')
    starting_price = forms.DecimalField(max_digits=7, decimal_places=2)
    picture = forms.URLField(label='Picture' ,required=False, widget=forms.TextInput(attrs={'placeholder': 'https://mysite.com/my-pic.jpg'}))

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-3'

    
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea-small', 'placeholder': 'Add a Comment...'}), label='')
from django import forms
from .models import Wantoitem

class WantoitemForm(forms.ModelForm):
    class Meta:
        model = Wantoitem
        fields = ('maker_name','item_name','tag', 'slug')

class ContactForm(forms.Form):
   name = forms.CharField(label='お名前', max_length=50)
   email = forms.EmailField(label='メールアドレス',)
   message = forms.CharField(label='メッセージ', widget=forms.Textarea)
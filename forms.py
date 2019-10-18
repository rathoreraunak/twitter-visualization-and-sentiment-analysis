from django import forms

class userinput(forms.Form):
    q=forms.CharField(required=True,max_length=100,label='Input #hashtag')

class userinputtext(forms.Form):
    q = forms.CharField(required=True, max_length=100, label='Enter Text')
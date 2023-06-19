from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label = "", required=False, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class PageForm(forms.Form):
    page_name = forms.CharField(label = "", required=False, widget=forms.TextInput(attrs={'placeholder': 'Page Title', 'class':'col-sm-11', 'style':'margin-bottom:9px;'}))
    page_body = forms.CharField(label = "", required= False,
                                widget=forms.Textarea(
                                    attrs={'placeholder': 'Enter markdown text', 'class':'col-sm-11'}
                                ))
    

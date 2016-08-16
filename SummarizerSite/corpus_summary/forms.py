from django import forms

# deffining this class to inherit from forms.ModelForm 
#class PostDocument(forms.ModelForm):
class PostDocument(forms.Form):
    """
    Since this form is inheriting from forms.Form we set it's named residents here'
    """
    class Meta:
        #model = ''
        fields = ['text']
        #text = forms.CharField(max_length = 5000)
        widgets = {
            'text': forms.TextInput(
                attrs = {
                    'id': 'post-text',
                    'required': True,
                    'placeholder': 'Text Body to summarize...'
                }
            ),
        }
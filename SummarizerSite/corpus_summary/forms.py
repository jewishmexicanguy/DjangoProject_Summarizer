from django import forms

class PostDocument(forms.ModelForm):
    class Meta:
        model = ''
        fields = ['text']
        widgets = {
            'text': forms.TextInput(
                attrs = {
                    'id': 'post-text',
                    'required': True,
                    'placeholder': 'Text Body to summarize...'
                }
            ),
        }

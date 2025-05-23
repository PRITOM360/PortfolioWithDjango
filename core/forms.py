from django import forms
from .models import Contact
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class ContactForm(forms.ModelForm):
    """Form for contact submissions"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'subject',
            'message',
            Div(
                Submit('submit', 'Send Message', css_class='bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'),
                css_class='text-center mt-4'
            )
        )
        
        # Add tailwind classes to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
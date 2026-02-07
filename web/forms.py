from django import  forms
from phonenumber_field.formfields import PhoneNumberField, country_code
from django.forms.widgets import PasswordInput, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Contact
from django.contrib.auth import get_user_model



class PhoneValidator(RegexValidator):
    regex = r'^\d{17}$'
    message = 'Invalid phone number'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'website', 'company_name', 'subject', 'message']

        first_name = forms.CharField(widget=forms.TextInput(), required=True)
        last_name = forms.CharField(widget=forms.TextInput(), required=True)
        email = forms.CharField(widget=forms.TextInput(), required=True)
        phone_number = forms.CharField(validators=[PhoneValidator()], required=True)
        website = forms.CharField(widget=forms.URLInput(), required=True)
        company_name = forms.CharField(widget=forms.TextInput(), required=True)
        subject = forms.CharField(widget=forms.TextInput(), required=True)
        message = forms.CharField(widget=forms.Textarea(), required=True)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Contact.objects.filter(email=email).exists():
          raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email
        
    def clean_name(self):
        name = self.changed_data['name']
        return name.strip()  #Removes spaces    
       
User = get_user_model()    


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required.inform a valid email address.')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
        first_name = forms.CharField(widget=forms.TextInput(), required=True)
        username = forms.CharField(widget=forms.TextInput(), required=True)
        email = forms.EmailField(widget=forms.TextInput(), required=True)
        password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
        
      
      
def signup(self):
    cad = self.cleaned_data
    if User.objects.filter(password=cad.get('password')).exists():
        self.add_error('password', 'Password already exists.')
        return cad
    
    # if cad.get('password1') != cad.get('password2'):
    #     self.add_error('password', 'Passwords do not exist.')
    #     return cad
    
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    passWord = forms.CharField(widget=forms.PasswordInput(), required=True)
    remember_me = forms.BooleanField(required=False)




class CustomPasswordResetForm(PasswordResetForm):
    def get_user(self, email):
        try:
           return self.get_users(email)
        except User.DoesNotExist:
            return None
    
    def save(self, domain_override = None, 
              subject_template_name = 'registration/password_reset_subject.txt', 
              email_template_name = 'registration/password_reset_email.html', 
              use_https = False, token_generator = default_token_generator, 
              from_email = None, request = None, html_email_template_name = None, 
              extra_email_context = None):
        """
        Generate a one-use only link for resetting password and send it to
        the user.
        """   
        email = self.cleaned_data['email']
        for user in self.get_user(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain 
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,   # I need to fix the domain name.
                'site_name': site_name,  # I need to fix the site name.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
                }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
                )
    
def send_mail(self, subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    subject = render_to_string(subject_template_name, context)
    # Email subject *must not* contain new lines.
    subject = ''.join(subject.splitlines())
    body = render_to_string(email_template_name, context)
    
    email_message = EmailMessage(subject, body, to=[to_email])
    email_message.send()
    
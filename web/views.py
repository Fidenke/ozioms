from django.shortcuts import render, redirect
from urllib3 import request
from .models import *
from django.contrib.auth.models import auth, User
from django.http import HttpResponse
from django.db import IntegrityError
from django.urls import reverse_lazy
import uuid
from django.conf import settings
from django.template.loader import render_to_string
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout
from  allauth.account.views import SignupView
from allauth.account import app_settings


class CustomSignupView(SignupView):
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['custom_message'] = 'Create an Account'
      return context

    def form_valid(self, form):
      #here you can add custom logic before saving
      response = super().form_valid(form)

      if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
        messages.info(
          self.request, 
          "Please verify your email address to complete the registration."
        )
      else:
        messages.success(
          self.request,
          f"Welcome {form.cleaned_data['username']}! Your Account created successfully."
        )  
      return response


@login_required(login_url='login')
def home(request):
  return render(request, 'home/index.html')


def signupView(request):
  if request.method == 'POST':
    first_name = request.POST.get('firstName').strip()
    username = request.POST.get('username').strip()
    email = request.POST.get('email').strip()
    # checkbox = request.POST.get('is_active')
    password = request.POST.get('password').strip()

    user_data_has_error = False

    if User.objects.filter(username=username).exists():
      user_data_has_error = True
      messages.error(request, "Username already exists.")
                
    if User.objects.filter(email=email).exists():
      user_data_has_error = True
      messages.error(request, "Email already exists.")
              
    if len(password) < 5:
      user_data_has_error = True
      messages.error(request, "Password must be at least 5 characters long.")
          
    if user_data_has_error:
      return redirect('signup')
    else:
      new_user = User.objects.create_user(
        first_name=first_name,
        email=email,
        # checkbox=checkbox,
        username=username,
        password=password,
      )
      new_user.save()
      messages.success(request, "Account created successfully!")
      return redirect('login') 
    
  return render(request, 'auth/signup.html')  


def loginView(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      auth_login(request, user)
      messages.success(request, "Logged in successfully!")
      return redirect('home')
    else:
      messages.error(request, "Invalid username or password.")
      return redirect('login')
    
  return render(request, 'auth/login.html')



def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verify if email exists in the database
        try:
            user = User.objects.get(email=email) 
            
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()
            
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f"{request.build_absolute_uri(password_reset_url)}"
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'   # we replace password_reset_url with full_password_reset_url to generate absolute url.
            
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,      # Email sender
                [email]   # Email receiver
            )  
            
            email_message.fail_silently = True
            email_message.send()
            
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)
                
            
        except User.DoesNotExist:
            messages.error(request, f"No user with the email '{email}' found")
            return redirect('forgot-password') 
                  
    return render(request, 'auth/forgot_password.html')


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'auth/password_reset_sent.html')
    else:
        # redirect to forgot password page if reset id is not valid
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
       
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            passwords_have_error = False
            
            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')
                
            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')
                
            
            # Check to make sure link has not expired
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=30)
                
            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired.')
                
                  
            if passwords_have_error:
                return redirect('reset-password', reset_id=password_reset_id.reset_id)    #I replace reset_id with password_reset_id to fix the error.
            passwords_match = password == confirm_password
            password_is_valid = len(password) >= 5
            
            if passwords_match and password_is_valid:
                reset_id.user.set_password(password)
                #user = password_reset_id.user
                #user.set_password(password)
                #user.save()
                reset_id.user.save()
                reset_id.delete()
                messages.success(request, 'Password reset successfully')
                return redirect('login')
            else:
                messages.error(request, 'Password must be at least 5 characters long and match the confirmation')
                return redirect('reset-password', reset_id=reset_id.reset_id)      
    
    
    except PasswordReset.DoesNotExist:
        
         # redirect to forgot password page if reset id is not valid
         messages.error(request, 'Invalid reset id')
         return redirect('forgot-password')

  #return render(request, 'auth/reset_password.html')




login_required(login_url='/login/')
def contact(request):
    if request.method == "POST":
      contacts = Contact()

      first_name = request.POST.get('first_name').strip()
      last_name = request.POST.get('last_name').strip()
      email = request.POST.get('email').strip()
      website = request.POST.get('website').strip()
      company_name = request.POST.get('company_name').strip()
      phone_number = request.POST.get('phone_number').strip()
      subject = request.POST.get('subject').strip()
      message = request.POST.get('message').strip()

      user_data_has_error = False

      if User.objects.filter(first_name=first_name).exists():
       user_data_has_error = True
       messages.error(request, "First name already exists.")

      if User.objects.filter(last_name=last_name).exists():
         user_data_has_error = True
         messages.error(request, "Last name already exists.")   

      # Here you can handle the form data, e.g., save it to the database or
      if User.objects.filter(email=email):
        messages.error(request, 'The same email address, please change the email.')

      try:
        contacts.first_name = first_name
        contacts.last_name = last_name
        contacts.email = email
        contacts.subject = subject
        contacts.phone_number = phone_number
        contacts.company_name = company_name
        contacts.website = website
        contacts.message = message

      
        messages.success(request, 'Your message has been submitted successfully. Thanks!')
        contacts.save()  # The error for contact page when submitted is pointed here.

        return redirect('home')

      except ValidationError as e:
        if user_data_has_error:
          messages.error(request, e.messages)
          contacts = ContactForm()   #return redirect('contact')
          return redirect('signup')

    return render(request, 'abc/contact.html') 

def privacy(request):
    return render(request, 'legal/privacy.html')

def terms(request):
    return render(request, 'legal/terms.html')

def logoutView(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


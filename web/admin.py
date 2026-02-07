from django.contrib import admin
from .models import *


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'website', 'company_name', 'subject', 'message')

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_id', 'created_when')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('image', 'name', 'description')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'bio', 'location', 'birth_date')

class userTestimonialAdmin(admin.ModelAdmin):
    list_display = ('image', 'name', 'designation', 'message')    





admin.site.register(Contact, ContactAdmin)

admin.site.register(PasswordReset, PasswordResetAdmin)

admin.site.register(userTestimonial, userTestimonialAdmin)


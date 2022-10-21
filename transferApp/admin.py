from django.contrib import admin
from .models import Profile,History,EmailVerification
#Register your models here.
admin.site.register(Profile)
admin.site.register(History)
admin.site.register(EmailVerification)
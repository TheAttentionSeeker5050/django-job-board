from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# import models
from .models import CompanyAdmin
# from django.contrib.auth.models import User

# Register your models here.
admin.site.register(CompanyAdmin)
admin.site.register(CustomUser, UserAdmin)
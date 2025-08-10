from django.contrib import admin
from .models import BlogModel, MailModel, Customer

# Register your models here.
admin.site.register(BlogModel)
admin.site.register(MailModel)
admin.site.register(Customer)

#
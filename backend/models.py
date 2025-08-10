from django.db import models
from django.utils.text import slugify 
from django.utils import timezone
import os


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="BlogImages/", blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


class MailModel(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    signature = models.TextField(blank=True, null=True)
    template = models.FileField(upload_to="MailTemplates/", blank=True, null=True)
    selected_for = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    def delete(self, *args, **kwargs):
        # Delete the template file when deleting the mail
        if self.template:
            if os.path.isfile(self.template.path):
                os.remove(self.template.path)
        super().delete(*args, **kwargs)


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    email = models.EmailField()
    sms_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_sms_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.contact_number}"

    def mark_sms_sent(self):
        """Mark SMS as sent and update timestamp"""
        self.sms_status = True
        self.sent_sms_at = timezone.now()
        self.save()
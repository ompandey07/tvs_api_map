from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import BlogModel, MailModel, Customer
import os


# ======================================================================
# AUTHENTICATION SERIALIZERS
# ======================================================================

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with email and password
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            raise serializers.ValidationError('Please enter both email and password')
        
        # Handle default admin login
        DEFAULT_EMAIL = 'admin@tvs.com'
        DEFAULT_PASSWORD = 'admin@1200'
        DEFAULT_USERNAME = 'admin'
        
        if email == DEFAULT_EMAIL.lower() and password == DEFAULT_PASSWORD:
            user = authenticate(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
            if user is not None and user.is_active:
                data['user'] = user
                return data
        
        # For other users, find by email
        try:
            user_obj = User.objects.get(email__iexact=email)
            username = user_obj.username
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        
        # Authenticate using username and password
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError('Your account has been deactivated')
        else:
            raise serializers.ValidationError('Invalid email or password')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['id', 'date_joined']


# ======================================================================
# BLOG SERIALIZERS
# ======================================================================

class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogModel with image handling
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogModel
        fields = ['id', 'title', 'content', 'image', 'image_url', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'image_url']
    
    def get_image_url(self, obj):
        """Get the full URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_title(self, value):
        """Validate blog title"""
        if not value or not value.strip():
            raise serializers.ValidationError('Blog title is required')
        return value.strip()


class BlogListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for blog lists
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogModel
        fields = ['id', 'title', 'image_url', 'slug', 'created_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


# ======================================================================
# SMS/MAIL SERIALIZERS
# ======================================================================

class MailSerializer(serializers.ModelSerializer):
    """
    Serializer for MailModel (SMS templates)
    """
    template_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MailModel
        fields = ['id', 'subject', 'content', 'signature', 'template', 'template_url', 'selected_for', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'template_url']
    
    def get_template_url(self, obj):
        """Get the full URL for the template file"""
        if obj.template:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.template.url)
            return obj.template.url
        return None
    
    def validate_subject(self, value):
        """Validate SMS subject"""
        if not value or not value.strip():
            raise serializers.ValidationError('SMS subject is required')
        return value.strip()
    
    def validate_content(self, value):
        """Validate SMS content"""
        if not value or not value.strip():
            raise serializers.ValidationError('SMS content is required')
        return value.strip()


class MailListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for mail/SMS lists
    """
    class Meta:
        model = MailModel
        fields = ['id', 'subject', 'selected_for', 'created_at']


class MailToggleSerializer(serializers.Serializer):
    """
    Serializer for toggling SMS template selection
    """
    selected = serializers.BooleanField()
    
    def validate(self, data):
        # Add any custom validation logic here
        return data


# ======================================================================
# CUSTOMER SERIALIZERS
# ======================================================================

class CustomerSerializer(serializers.ModelSerializer):
    """
    Full serializer for Customer model
    """
    sent_sms_at_formatted = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'contact_number', 'address', 'email', 
            'sms_status', 'created_at', 'updated_at', 'sent_sms_at',
            'sent_sms_at_formatted', 'created_at_formatted', 'updated_at_formatted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'sent_sms_at']
    
    def get_sent_sms_at_formatted(self, obj):
        return obj.sent_sms_at.strftime('%Y-%m-%d %H:%M:%S') if obj.sent_sms_at else None
    
    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else None
    
    def get_updated_at_formatted(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S') if obj.updated_at else None
    
    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Full name is required')
        return value.strip()
    
    def validate_contact_number(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Contact number is required')
        return value.strip()
    
    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Email is required')
        return value.strip()
    
    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Address is required')
        return value.strip()


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for customer lists
    """
    sms_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'contact_number', 'email', 'sms_status', 'sms_status_display', 'created_at']
    
    def get_sms_status_display(self, obj):
        return "Sent" if obj.sms_status else "Pending"


class CustomerImportSerializer(serializers.Serializer):
    """
    Serializer for customer data import from Excel
    """
    excel_file = serializers.FileField()
    
    def validate_excel_file(self, value):
        """Validate uploaded Excel file"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError('Please upload a valid Excel file (.xlsx or .xls)')
        
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum allowed size is 10MB')
        
        return value


class DuplicateHandlingSerializer(serializers.Serializer):
    """
    Serializer for handling duplicate resolution during import
    """
    duplicate_action = serializers.ChoiceField(choices=['replace', 'ignore', 'cancel'])
    
    def validate_duplicate_action(self, value):
        if value not in ['replace', 'ignore', 'cancel']:
            raise serializers.ValidationError('Invalid duplicate action')
        return value


# ======================================================================
# DASHBOARD SERIALIZERS
# ======================================================================

class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for dashboard statistics
    """
    total_customers = serializers.IntegerField(read_only=True)
    sms_sent_count = serializers.IntegerField(read_only=True)
    sms_pending_count = serializers.IntegerField(read_only=True)
    total_blogs = serializers.IntegerField(read_only=True)
    total_sms_templates = serializers.IntegerField(read_only=True)
    selected_sms_template = serializers.CharField(read_only=True, allow_null=True)
    
    class Meta:
        fields = [
            'total_customers', 'sms_sent_count', 'sms_pending_count',
            'total_blogs', 'total_sms_templates', 'selected_sms_template'
        ]


# ======================================================================
# SEARCH SERIALIZERS
# ======================================================================

class SearchSerializer(serializers.Serializer):
    """
    Serializer for search functionality across different models
    """
    search = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(required=False, min_value=1)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=100)
    
    def validate_search(self, value):
        if value:
            return value.strip()
        return value


# ======================================================================
# FILE OPERATION SERIALIZERS
# ======================================================================

class FileOperationSerializer(serializers.Serializer):
    """
    Serializer for file operations (upload, download, delete)
    """
    action = serializers.ChoiceField(choices=['export_format', 'export_data', 'import_data'])
    
    def validate_action(self, value):
        if value not in ['export_format', 'export_data', 'import_data']:
            raise serializers.ValidationError('Invalid file operation action')
        return value
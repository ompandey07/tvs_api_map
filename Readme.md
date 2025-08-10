# TVS Site API Map

A comprehensive Django REST API for managing blogs, SMS templates, and customer data with import/export functionality. Built for the TVS Site administrative dashboard.

## 🚀 Tech Stack

- **Python** - Core programming language
- **Django REST Framework** - Powerful API framework
- **CORS Headers** - Cross-origin resource sharing
- **Pandas** - Data manipulation and analysis
- **Bleach** - HTML sanitization and security
- **Pillow** - Image processing and handling
- **Serializers** - Data validation and transformation
- **OpenPyXL** - Excel file operations
- **Token Authentication** - Secure API access

## 📁 Repository

**GitHub:** [https://github.com/ompandey07/tvs_api_map](https://github.com/ompandey07/tvs_api_map)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ompandey07/tvs_api_map.git
cd tvs_api_map
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Configure Settings
Add the following to your `settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    
    # Your app
    'backend',
]

# Add CORS middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True
```

### 5. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/api/`

## 📋 Requirements.txt

```
Django>=4.2.0
djangorestframework>=3.14.0
django-cors-headers>=3.13.0
pandas>=1.3.0
openpyxl>=3.0.9
Pillow>=9.0.0
bleach>=5.0.0
```

## 🔐 Authentication

### Default Admin Credentials
- **Email:** `admin@tvs.com`
- **Password:** `admin@1200`

### Getting Authentication Token
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "email": "admin@tvs.com",
    "password": "admin@1200"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Welcome back, Admin!",
    "token": "your-auth-token-here",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@tvs.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

### Using Token in Requests
Include the token in the Authorization header:
```
Authorization: Token your-auth-token-here
```

## 🛠️ API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login with email/password |
| POST | `/api/auth/logout/` | Logout and invalidate token |
| POST | `/api/auth/token/` | Alternative token auth |

### Dashboard Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/` | Get dashboard statistics |

### Blog Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/blogs/` | List all blogs (with pagination & search) |
| POST | `/api/blogs/` | Create new blog |
| GET | `/api/blogs/{id}/` | Get specific blog |
| PUT | `/api/blogs/{id}/` | Update specific blog |
| PATCH | `/api/blogs/{id}/` | Partial update blog |
| DELETE | `/api/blogs/{id}/` | Delete blog |

### SMS Template Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/mails/` | List SMS templates (with pagination & search) |
| POST | `/api/mails/` | Create new SMS template |
| GET | `/api/mails/{id}/` | Get specific SMS template |
| PUT | `/api/mails/{id}/` | Update SMS template |
| PATCH | `/api/mails/{id}/` | Partial update SMS template |
| DELETE | `/api/mails/{id}/` | Delete SMS template |
| POST | `/api/mails/{id}/toggle_selected/` | Toggle selection status |
| POST | `/api/mails/{id}/confirm_switch/` | Force switch to template |

### Customer Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/` | List customers (with pagination & search) |
| GET | `/api/customers/?action=export_format` | Download Excel template |
| GET | `/api/customers/?action=export_data` | Download customers data |
| POST | `/api/customers/` (action=import_data) | Import from Excel |
| POST | `/api/customers/` (action=handle_duplicates) | Handle duplicates |

### Utility Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check (no auth required) |
| GET | `/api/documentation/` | API documentation |

## 📊 Query Parameters

### Search & Pagination
- `?search=<query>` - Search across relevant fields
- `?page=<number>` - Page number for pagination
- `?page_size=<number>` - Items per page (max 100)

### Examples
```bash
# Search blogs
GET /api/blogs/?search=technology&page=1

# Search customers
GET /api/customers/?search=john&page_size=10

# Search SMS templates
GET /api/mails/?search=welcome
```

## 📝 Usage Examples

### 1. Create a Blog Post
```bash
POST /api/blogs/
Authorization: Token your-token
Content-Type: application/json

{
    "title": "My New Blog Post",
    "content": "This is the content of my blog post."
}
```

### 2. Upload Blog with Image
```bash
POST /api/blogs/
Authorization: Token your-token
Content-Type: multipart/form-data

FormData:
- title: "Blog with Image"
- content: "Content here"
- image: [image file]
```

### 3. Create SMS Template
```bash
POST /api/mails/
Authorization: Token your-token
Content-Type: application/json

{
    "subject": "Welcome SMS",
    "content": "Welcome {customer_name} to our service!",
    "signature": "Best regards, TVS Team"
}
```

### 4. Import Customers from Excel
```bash
POST /api/customers/
Authorization: Token your-token
Content-Type: multipart/form-data

FormData:
- action: "import_data"
- excel_file: [Excel file with customer data]
```

## 📋 Excel Import Format

### Required Columns
| Column Name | Description | Required |
|-------------|-------------|----------|
| FULL NAME | Customer's full name | Yes |
| CONTACT NUMBER | Phone number | Yes |
| ADDRESS | Customer address | Yes |
| EMAIL | Email address | Yes |

### Sample Excel Data
```
FULL NAME       | CONTACT NUMBER | ADDRESS                    | EMAIL
John Doe        | 1234567890     | 123 Main St, City, State  | john@email.com
Jane Smith      | 0987654321     | 456 Oak Ave, Town, State  | jane@email.com
```

## 🔧 Configuration Options

### File Upload Settings
```python
# Maximum file upload size
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_EXCEL_EXTENSIONS = ['.xlsx', '.xls']
```

### Pagination Settings
```python
PAGINATION_SETTINGS = {
    'CUSTOMERS_PER_PAGE': 15,
    'BLOGS_PER_PAGE': 10,
    'SMS_TEMPLATES_PER_PAGE': 5,
}
```

## 🚀 Deployment

### Production Settings
```python
# In production settings
DEBUG = False
CORS_ALLOW_ALL_ORIGINS = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# Disable browsable API in production
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]
```

### Environment Variables
```bash
export DJANGO_ENV=production
export SECRET_KEY=your-secret-key
export DEBUG=False
```

## 🧪 Testing

### Using curl
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "admin@tvs.com", "password": "admin@1200"}'

# Get dashboard (replace TOKEN with actual token)
curl -X GET http://localhost:8000/api/dashboard/ \
-H "Authorization: Token TOKEN"
```

### Using Python requests
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'email': 'admin@tvs.com',
    'password': 'admin@1200'
})
token = response.json()['token']

# Use token
headers = {'Authorization': f'Token {token}'}
dashboard = requests.get('http://localhost:8000/api/dashboard/', headers=headers)
```

## 📄 Response Format

All API responses follow this standard format:

### Success Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": { ... }
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error message here",
    "errors": { ... }  // Field-specific errors
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- **GitHub Issues:** [https://github.com/ompandey07/tvs_api_map/issues](https://github.com/ompandey07/tvs_api_map/issues)
- **Repository:** [https://github.com/ompandey07/tvs_api_map](https://github.com/ompandey07/tvs_api_map)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Django REST Framework**
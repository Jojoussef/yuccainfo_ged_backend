# YuccaInfo GED Backend

A Document Management System (GED - Gestion Électronique des Documents) backend built with Django REST Framework that provides document storage, organization, and intelligent classification services.

## Overview

This system allows users to upload, store, and manage documents while automatically extracting text and classifying documents by type. The system features role-based access control, JWT authentication, and a RESTful API.

## Features

- **Document Management**

  - Upload & store documents
  - Automatic text extraction from images/PDFs using Tesseract OCR
  - AI-powered document classification
  - Document categorization

- **User Management**

  - JWT-based authentication
  - Role-based access control (Admin and User groups)
  - Registration and logout functionality

- **API**
  - RESTful API for document and category operations
  - Permission-based access to resources

## Technical Stack

- **Framework**: Django 5.2, Django REST Framework 3.16.0
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework_simplejwt)
- **Text Extraction**: pytesseract 0.3.13
- **Document Classification**: Transformers (facebook/bart-large-mnli model)
- **Other**:
  - django-cors-headers for CORS support
  - python-dotenv for environment configuration

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd yuccainfo_ged_backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root with the following variables:

   ```
   DB_NAME=yuccainfo_ged_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   ```

5. **Set up the database**

   ```bash
   # Create PostgreSQL database
   createdb yuccainfo_ged_db

   # Run migrations
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register/`: Register a new user
- `POST /api/auth/logout/`: Logout the current user
- `POST /api/token/`: Obtain JWT token pair
- `POST /api/token/refresh/`: Refresh JWT token

### Documents

- `GET /api/documents/`: List all documents (filtered by user permissions)
- `POST /api/documents/`: Upload a new document
- `GET /api/documents/{id}/`: Retrieve a specific document
- `PUT /api/documents/{id}/`: Update a specific document
- `DELETE /api/documents/{id}/`: Delete a specific document

### Categories

- `GET /api/categories/`: List all categories
- `POST /api/categories/`: Create a new category
- `GET /api/categories/{id}/`: Retrieve a specific category
- `PUT /api/categories/{id}/`: Update a specific category
- `DELETE /api/categories/{id}/`: Delete a specific category

## Permission System

The system uses Django's built-in permission system with custom extensions:

1. **Admin Group**: Full access to all documents and categories
2. **User Group**: Access limited to owned documents
3. Custom `IsAdminOrOwner` permission to ensure users can only access their own documents

## Document Classification

When a document is uploaded, the system:

1. Extracts text using Tesseract OCR if it's an image or PDF
2. Uses a zero-shot classification model to determine document type
3. Categorizes the document automatically based on content
4. Assigns it to one of these categories: invoice, contract, letter, report, receipt, memo, email, presentation, or other

## Requirements

- Python 3.x
- PostgreSQL
- Tesseract OCR installed on the system

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request

## License

[Your license information]

# School Bud - CS Education Platform

A comprehensive web-based platform for computer science education that combines Stack Overflow-like Q&A functionality with GitHub integration, user profiles, analytics, and more.

## Features

- **Q&A System**: Ask questions, provide answers, and vote on content
- **GitHub Integration**: Connect with GitHub, showcase repositories, and discuss projects
- **User Profiles**: Personalized profiles with activity tracking and GitHub connections
- **Analytics Dashboard**: Track course activity, GitHub engagement, and user participation
- **Markdown Support**: Rich text formatting with syntax highlighting for code snippets
- **Responsive Design**: Modern UI that works across devices

## Tech Stack

- **Backend**: Django, Django REST Framework, PostgreSQL
- **Frontend**: React, Bootstrap, Webpack
- **Authentication**: Django Social Auth (GitHub OAuth)
- **Analytics**: Custom event tracking

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 16+ and npm (for frontend development)
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/tirips12/School_Bud.git
cd School_Bud
```

### 2. Set up Python environment

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

- Install PostgreSQL if not already installed
- Create a database for the project
- Update the database settings in `cseducation/cseducation/settings.py` or use environment variables

```python
# Example database configuration in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'schoolbud',  # your database name
        'USER': 'postgres',   # your database user
        'PASSWORD': 'password', # your database password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Set up frontend (if developing)

```bash
cd cseducation/frontend
npm install
npm run build
```

### 5. Run migrations and create superuser

```bash
cd cseducation  # Make sure you're in the directory with manage.py
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to access the application.

## Environment Variables

For production or to use GitHub integration, you'll need to set up the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string (optional, can use settings.py)
- `GITHUB_KEY`: GitHub OAuth App Client ID
- `GITHUB_SECRET`: GitHub OAuth App Client Secret

## Admin Access

Access the admin interface at http://127.0.0.1:8000/admin/ using the superuser credentials created earlier.
- username: admin
- password: admin123
## License

This project is licensed under the MIT License - see the LICENSE file for details.

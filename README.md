# Personal Portfolio Website

A professional Django-based portfolio website showcasing skills, projects, experience, and blog.

## Features

- Responsive design with dark/light mode
- Home page with hero section and key information
- About Me section with education and experience
- Projects showcase with filtering by category/technology
- Skills section organized by category
- Blog with categories, tags, and comments
- Contact form with email notifications
- Admin dashboard for content management
- SEO-friendly structure

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: Tailwind CSS, Alpine.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Text Editor**: CKEditor for rich text content
- **Form Handling**: django-crispy-forms with Tailwind pack

## Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables
   ```
   cp .env.example .env
   # Edit the .env file with your specific settings
   ```

5. Setup the database
   ```
   python manage.py migrate
   ```

6. Create a superuser
   ```
   python manage.py createsuperuser
   ```

7. Install Tailwind CSS dependencies
   ```
   python manage.py tailwind install
   ```

8. Start the development server
   ```
   python manage.py tailwind start  # In one terminal
   python manage.py runserver       # In another terminal
   ```

9. Visit `http://127.0.0.1:8000` in your browser

## Deployment

For production deployment:

1. Set `DEBUG=False` in your .env file
2. Configure PostgreSQL database settings
3. Set up proper email settings
4. Collect static files:
   ```
   python manage.py collectstatic
   ```
5. Deploy using your preferred method (e.g., Heroku, DigitalOcean, AWS)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
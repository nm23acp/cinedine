# CineDine

CineDine is a Django web application that brings movie discovery and restaurant browsing together in one place. Users can explore popular movies, browse restaurant listings and submit movie ticket bookings.

Movie information is retrieved from The Movie Database (TMDB), while restaurant and booking records are managed through Django models and SQLite.

## Features

- Popular movie listings retrieved from the TMDB API.
- Restaurant listings backed by Django models and SQLite.
- Individual restaurant detail pages.
- Restaurant image uploads.
- Movie ticket booking using Django ModelForms.
- Django authentication views for login and logout.
- Input validation and automated tests.
- External API timeouts and graceful handling of TMDB errors.

## Technology Stack

- Python
- Django
- SQLite
- HTML and CSS
- The Movie Database (TMDB) API
- Requests

## Local Setup

**Requirements:** A Python version supported by Django 6.0.

1. Clone the repository and enter the project directory.

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.

   **Windows PowerShell:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`. Add your own TMDB API key and generate a new Django secret key.

   Generate a secret key using:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Never commit your `.env` file or share your credentials.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create an administrator account:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

   Restaurant records can be added through the Django admin panel at `/admin/`.

If `TMDB_API_KEY` is missing or the TMDB service is unavailable, the website remains accessible, but movie listings may be empty.

## Running Tests

Run the automated tests with:

```bash
python manage.py test
```

The tests cover booking form validation, successful and unsuccessful booking submissions, TMDB success and failure handling, and restaurant detail pages.

## Security Notes

- Keep `.env`, database files, uploaded media and credentials out of version control.
- Use a newly generated `DJANGO_SECRET_KEY`.
- Rotate credentials if they have been exposed.
- Set `DJANGO_DEBUG=False` for production.
- Configure HTTPS, allowed hosts and deployment-specific security settings before deployment.

This is an educational portfolio project, not a production-ready ticketing platform. It does not integrate with live cinema seat inventory or payment providers.

## Project Structure

```text
CineDine/
├── cinedine/
│   ├── settings.py
│   └── urls.py
├── core/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Credits

Movie metadata and poster images are provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).

This project is not endorsed or certified by TMDB.
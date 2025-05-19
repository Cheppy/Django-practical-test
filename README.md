# Task 1: Django Fundamentals

1. **Create a New Django Project**
   - Name it something like `CVProject`.
   - Use the Python version set up in **Task 2** and the latest stable Django release.
   - Use **SQLite** as your database for now.

2. **Create an App and Model**
   - Create a Django app (for example, `main`).
   - Define a `CV` model with fields like `firstname`, `lastname`, `skills`, `projects`, `bio`, and `contacts`.
   - Organize the data in a way that feels efficient and logical.

3. **Load Initial Data with Fixtures**
   - Create a fixture that contains at least one sample `CV` instance.
   - Include instructions in `README.md` on how to load the fixture.

4. **List Page View and Template**
   - Implement a view for the main page (e.g., `/`) to display a list of CV entries.
   - Use any CSS library to style them nicely.
   - Ensure the data is retrieved from the database efficiently.

5. **Detail Page View**
   - Implement a detail view (e.g., `/cv/<id>/`) to show all data for a single CV.
   - Style it nicely and ensure efficient data retrieval.

6. **Tests**
   - Add basic tests for the list and detail views.
   - Update `README.md` with instructions on how to run these tests.

# Task 2: PDF Generation Basics

1. Choose and install any HTML-to-PDF generating library or tool.

2. Add a "Download PDF" button on the CV detail page that allows users to download the CV as a PDF.

# Task 3: REST API Fundamentals

1. Install **Django REST Framework** (DRF).

2. Create CRUD endpoints for the `CV` model (create, retrieve, update, delete).

3. Add tests to verify that each CRUD action works correctly.

# Task 4: Middleware & Request Logging

1. **Create a `RequestLog` Model**
   - You can put this in the existing app or a new app (e.g., `audit`).
   - Include fields such as `timestamp`, HTTP `method`, `path`, and optionally other details like query string, remote IP, or logged-in user.

2. **Implement Logging Middleware**
   - Write a custom Django middleware class that intercepts each incoming request.
   - Create a `RequestLog` record in the database with the relevant request data.
   - Keep it efficient.

3. **Recent Requests Page**
   - Create a view (e.g., `/logs/`) showing the 10 most recent logged requests, sorted by timestamp descending.
   - Include a template that loops through these entries and displays their timestamp, method, and path.

4. **Test Logging**
   - Ensure your tests verify the logging functionality.

# Task 5: Template Context Processors

1. **Create `settings_context`**
   - Create a context processor that injects your entire Django settings into all templates.

2. **Settings Page**
   - Create a view (e.g., `/settings/`) that displays `DEBUG` and other settings values made available by the context processor.

# Task 6: Docker Basics

1. Use Docker Compose to containerize your project.
2. Switch the database from SQLite to PostgreSQL in Docker Compose.
3. Store all necessary environment variables (database credentials, etc.) in a `.env` file.

# Task 7: Celery Basics

1. Install and configure **Celery**, using Redis or RabbitMQ as the broker.
2. Add a Celery worker to your Docker Compose configuration.
3. On the CV detail page, add an email input field and a **'Send PDF to Email'** button to trigger a Celery task that emails the PDF.

# Task 8: OpenAI Basics

1. On the CV detail page, add a **'Translate'** button and a language selector.
2. Include these languages:  
   Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino,  
   Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama
3. Hook this up to an OpenAI translation API or any other translation mechanism you prefer.  
   The idea is to translate the CV content into the selected language.

# Task 9: Deployment

- Deploy this project to DigitalOcean or any other VPS.  

# CV Project

A Django-based CV management system that allows users to view and manage CVs.

## Features

- List view of all CVs with basic information
- Detailed view for each CV
- Responsive design using Bootstrap
- Clean and professional UI

## Installation

1. Install Poetry (if not already installed):
   ```bash
   # For macOS / Linux / WSL
   curl -sSL https://install.python-poetry.org | python3 -

   # For Windows PowerShell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```
   After installation, you may need to restart your terminal.

2. Clone the repository
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Run migrations:
   ```bash
   poetry run python manage.py migrate
   ```
5. Load sample data:
   ```bash
   poetry run python manage.py loaddata sample_cv
   ```

## Running the Development Server

```bash
poetry run python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Running Tests

The project includes a comprehensive test suite organized into unit and integration tests. To run the tests:

```bash
# Run all tests
poetry run python manage.py test main

# Run specific test categories
poetry run python manage.py test main.tests.unit  # Run unit tests only
poetry run python manage.py test main.tests.integration  # Run integration tests only
```

The test suite includes:

### Unit Tests
- Model tests (`main/tests/unit/test_models.py`)
  - CV model creation and validation
  - Timestamp handling
  - String representation

### Integration Tests
- View tests (`main/tests/integration/test_views.py`)
  - List view functionality
  - Detail view functionality
  - 404 handling for non-existent CVs
  - Template usage verification
  - Content display verification

## Project Structure

- `main/` - Main application directory
  - `models.py` - CV model definition
  - `views.py` - View classes for list and detail views
  - `urls.py` - URL routing configuration
  - `templates/` - HTML templates
    - `main/cv_list.html` - List view template
    - `main/cv_detail.html` - Detail view template
  - `fixtures/` - Sample data
    - `sample_cv.json` - Sample CV data

## Technologies Used

- Django 5.2.1
- Bootstrap 5.3.0
- SQLite (development database)
- Poetry (dependency management)

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Run migrations:
```bash
poetry run python manage.py migrate
```

3. Load sample data (optional):
```bash
poetry run python manage.py loaddata main/fixtures/sample_cv.json
```

4. Start the development server:
```bash
poetry run python manage.py runserver
```

5. To run in the docker:
```bash
docker compose -f docker-compose.yml build --no-cache && docker compose -f docker-compose.yml up -d --remove-orphans
```


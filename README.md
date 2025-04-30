# Commerce - E-commerce Auction Site

A Django-based e-commerce auction site where users can post auction listings, place bids on listings, comment on listings, and add listings to a watchlist.

## Features

- User authentication (register, login, logout)
- Create and manage auction listings
- Place bids on active listings
- Add/remove listings to/from watchlist
- Comment on listings
- Like listings
- View active listings by category
- Close auctions and declare winners

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd commerce
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the site at `http://localhost:8000`

## Project Structure

- `auctions/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL patterns
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JavaScript)
  - `admin.py` - Admin site configuration

## Technologies Used

- Django
- Python
- SQLite
- HTML/CSS
- JavaScript
- Bootstrap
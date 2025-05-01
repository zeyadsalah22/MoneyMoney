# MoneyMoney - E-commerce Auction Site

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
- View won auctions history

## Setup

1. Clone the repository:
```bash
git clone https://github.com/zeyadsalah22/MoneyMoney.git
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

## Project Design

### Database Models

The application uses the following Django models:

1. **User** (Custom User Model)
   - Extends Django's AbstractUser
   - User types: bidder, seller, or both
   - Fields: username, email, password, user_type

2. **Category**
   - Represents product categories
   - Fields: name, description, created_at
   - One-to-many relationship with Listings

3. **Listing**
   - Represents auction items
   - Fields: title, description, starting_price, current_price, image_url, status, created_at, end_date
   - Foreign keys: category, seller (User), winner (User)
   - One-to-many relationships with Bids, Comments, and Likes

4. **Bid**
   - Represents bids placed on listings
   - Fields: price, created_at
   - Foreign keys: bidder (User), listing (Listing)

5. **Comment**
   - Represents user comments on listings
   - Fields: comment, created_at
   - Foreign keys: writer (User), product (Listing)

6. **WatchList**
   - Represents items users are watching
   - Fields: created_at
   - Foreign keys: user (User), item (Listing)

7. **Like**
   - Represents user likes on listings
   - Fields: created_at
   - Foreign keys: user (User), listing (Listing)
   - Unique constraint on user and listing combination

### Views

The application implements the following views:

1. **Authentication Views**
   - `login_view`: Handles user login
   - `logout_view`: Handles user logout
   - `register`: Handles user registration with type selection

2. **Listing Views**
   - `index`: Displays active listings
   - `create`: Handles listing creation (seller-only)
   - `listing_page`: Displays detailed listing view with bids and comments
   - `close`: Allows sellers to close auctions
   - `won_auctions`: Displays auctions won by the current user

3. **Bidding and Watchlist Views**
   - `bid`: Handles bid placement
   - `watch`: Toggles items in watchlist
   - `watchlist`: Displays user's watchlist

4. **Category Views**
   - `category`: Lists all categories
   - `category_listings`: Shows listings in a specific category
   - `create_category`: API endpoint for category creation

5. **Comment Views**
   - `comment`: Handles comment creation
   - `delete_comment`: Handles comment deletion

6. **Like Views**
   - `like`: Toggles likes on listings

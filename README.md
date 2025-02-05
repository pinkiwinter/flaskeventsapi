# Events Management Backend API

This project is a backend system for managing events, built with **Python** and **Flask**. It includes simple and useful tools for user sign-up, event creation, joining or leaving events, leaving reviews, and admin actions. It is designed to be easy to expand and maintain, and shows how to create APIs with Flask.

## Key Features

1.  **User Authentication**
    
    -   Users can sign up and log in using secure tokens (JWT).
    -   Passwords are safely stored with encryption.
2.  **Event Management**
    
    -   Add, edit, start, end, or cancel events.
    -   Search events by host, status, title, or start time.
3.  **Participation Management**
    
    -   Users can join or leave events.
    -   Keeps track of how many people are in each event.
4.  **Review System**
    
    -   Users can rate and review events after they end.
    -   Stops users from leaving more than one review for the same event.
5.  **Admin Controls**
    
    -   Admins can remove bad events or reviews.
6.  **Error Handling**
    
    -   Handles errors in one place for easy-to-read messages.
    -   Custom messages for missing pages or server problems.
7.  **Testing**
    
    -   Detailed tests written with `pytest` to check everything works.
    -   Covers tricky situations to make sure the system is strong.

## Technologies

-   **Backend**:  Flask, Flask-JWT-Extended, Flask-Migrate, SQLAlchemy.
-   **Database**: PostgreSQL (can be changed to other databases).
-   **Validation**: Marshmallow.
-   **Testing**: Pytest.

## Project Structure

```
events/
├── app/
│   ├── models/         # Database setup
│   ├── routes/         # API endpoints
│   ├── schemas/        # Marshmallow schemas for data validation.
│   ├── __init__.py     
│   ├── auth.py         # User login and sign-up tools
│   └── config.py       # App settings
├── tests/              # Automated tests
├── pytest.ini          # Pytest configuration
├── .env                # Environment variables (e.g., secrets, database URL)             
└── run.py              # Runs the app

```

## Running the Project

- Install dependencies: `pip install -r requirements.txt`.

- Configure environment variables in a .env file (e.g., database URL, secret keys).

	```py
	APP_SECRET_KEY=

	DATABASE_URL=

	JWT_SECRET_KEY=

	TEST_DATABASE_URL=

	TEST_JWT_SECRET_KEY=
	```
	
- Initialize the database migrations: `flask db init`.

- Sync the database with models: `flask db upgrade`.

- Run the application: `flask run`.

- Test with pytest: `pytest`.

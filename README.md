# Book Store API

A REST API for an online book store designed as a layered monolithic application with a clear separation between API, business logic, data access, and persistence layers.


## Table of Contents

* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Quick Start](#quick-start)
  * [With Docker (Recommended)](#with-docker-recommended)
  * [Locally Without Docker](#locally-without-docker)
* [API Documentation](#api-documentation)
* [API Endpoints](#api-endpoints)
  * [Authentication](#authentication)
  * [Users](#users)
  * [Books](#books)
  * [Categories](#categories)
  * [Orders](#orders)
* [Request Examples](#request-examples)
* [Testing](#testing)
* [Environment Variables](#environment-variables)
* [Database Migrations](#database-migrations)
* [Notes](#notes)

## Technology Stack

| Technology           | Purpose                                 |
|----------------------|-----------------------------------------|
| Python 3.14          | Application runtime                     |
| FastAPI              | REST API framework                      |
| Pydantic v2          | Validation and serialization            |
| SQLAlchemy 2.0 Async | ORM and asynchronous database access    |
| PostgreSQL 16        | Relational database                     |
| Alembic              | Database migrations                     |
| JWT                  | Access and refresh token authentication |
| Passlib / bcrypt     | Password hashing and verification       |
| Pytest               | Automated testing                       |
| pytest-asyncio       | Async test support                      |
| Ruff                 | Linter and code formatter               |
| Docker               | Containerized application runtime       |
| Docker Compose       | Local multi-container environment       |

## Project Structure

```text
Book_Store_API/
├── alembic/
│   ├── versions/                 # Database migration revisions
│   ├── env.py                    # Alembic configuration for async migrations
│   └── script.py.mako            # Template used to generate new migration files
│
├── app/
│   ├── api/
│   │   ├── deps.py               # Dependency providers
│   │   ├── router.py             # Combines and registers API v1 routers
│   │   └── v1/
│   │       ├── auth.py            # Authentication endpoints
│   │       ├── books.py           # Book endpoints
│   │       ├── categories.py      # Category endpoints
│   │       ├── orders.py          # Order endpoints
│   │       └── users.py           # User endpoints
│   │
│   ├── core/
│   │   ├── config.py              # Application settings
│   │   ├── dependencies.py        # Authentication / authorization dependencies
│   │   └── security.py            # Password hashing and JWT helpers
│   │
│   ├── database/
│   │   ├── base.py                 # SQLAlchemy Base
│   │   ├── session.py              # Async engine and session factory
│   │   └── init_db.py              # Database initialization and default data setup
│   │
│   ├── exceptions/
│   │   ├── all_exceptions.py       # Application exception definitions
│   │   └── exception_handlers      # Global handlers for application exceptions 
│   │
│   ├── models/
│   │   ├── __init__.py             # Imports all models and makes them available to SQLAlchemy/Alembic
│   │   ├── user.py                 # User model
│   │   ├── book.py                 # Book model
│   │   ├── category.py             # Category model
│   │   ├── book_category.py        # Book/category association model
│   │   ├── order.py                # Order model
│   │   ├── order_item.py           # Order item model
│   │   ├── enums.py                # User and order enums
│   │   └── mixins.py               # Shared UUID/timestamp mixins
│   │
│   ├── repositories/
│   │   ├── base.py                 # Generic repository
│   │   ├── user.py                 # User data access
│   │   ├── book.py                 # Book data access
│   │   ├── category.py             # Category data access
│   │   ├── order.py                # Order data access
│   │   └── order_item.py           # Order item data access
│   │
│   ├── schemas/
│   │   ├── user.py                 # User and token schemas
│   │   ├── book.py                 # Book schemas
│   │   ├── category.py             # Category schemas
│   │   ├── order.py                # Order schemas
│   │   └── order_item.py            # Order item schemas
│   │
│   ├── services/
│   │   ├── base.py                 # Base service
│   │   ├── auth.py                 # Authentication business logic
│   │   ├── user.py                 # User business logic
│   │   ├── book.py                 # Book business logic
│   │   ├── category.py             # Category business logic
│   │   └── order.py                # Order business logic
│   │
│   └── main.py                     # FastAPI application entry point
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── test_security.py
│   ├── api/
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_books.py
│   │   ├── test_categories.py
│   │   └── test_orders.py
│   └── integration/
│       ├── conftest.py
│       ├── test_auth_service.py
│       ├── test_book_service.py
│       ├── test_category_service.py
│       └── test_order_service.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

## Quick Start

### With Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/badly-juice/Book_Store_API

# Start container
docker compose up --build -d
```

Follow container logs:

```bash
docker compose logs -f
```

### Locally Without Docker

A local run is possible when PostgreSQL is installed and available separately.

```bash
# Create virtual environment
python -m venv .venv
```

Activate virtual environment:

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure `.env.example`, apply migrations, and start the application:

```bash
# Apply migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:
```text
http://localhost:8000/docs
```
ReDoc:
```text
http://localhost:8000/redoc
```
OpenAPI schema:
```text
http://localhost:8000/openapi.json
```

## API Endpoints

### Authentication

| Method | Endpoint                | Description                                              | Access     |
|--------|-------------------------|----------------------------------------------------------|------------|
| POST   | `/api/v1/auth/register` | Register a new user                                      | All        |
| POST   | `/api/v1/auth/login`    | Authenticate a user and return access and refresh tokens | All        |
| POST   | `/api/v1/auth/refresh`  | Issue a new access/refresh token pair                    | Authorized |


### Users

| Method | Endpoint                  | Description                       | Access        |
|--------|---------------------------|-----------------------------------|---------------|
| GET    | `/api/v1/users/`          | Get all users                     | Administrator |
| GET    | `/api/v1/users/me`        | Get the current user's profile    | Authorized    |
| GET    | `/api/v1/users/{user_id}` | Get a user by ID                  | Administrator |
| PATCH  | `/api/v1/users/me`        | Update the current user's profile | Authorized    |
| PATCH  | `/api/v1/users/{user_id}` | Update a user's profile           | Administrator |


### Books

| Method | Endpoint                  | Description                         | Access        |
|--------|---------------------------|-------------------------------------|---------------|
| GET    | `/api/v1/books/`          | Get all books with their categories | All           |
| GET    | `/api/v1/books/{book_id}` | Get a single book                   | All           |
| POST   | `/api/v1/books/`          | Create a book                       | Administrator |
| PATCH  | `/api/v1/books/{book_id}` | Update a book                       | Administrator |
| DELETE | `/api/v1/books/{book_id}` | Delete a book                       | Administrator |


### Categories

| Method | Endpoint                           | Description           | Access        |
|--------|------------------------------------|-----------------------|---------------|
| GET    | `/api/v1/categories/`              | Get all categories    | All           |
| GET    | `/api/v1/categories/{category_id}` | Get a single category | All           |
| POST   | `/api/v1/categories/`              | Create a category     | Administrator |
| PATCH  | `/api/v1/categories/{category_id}` | Update a category     | Administrator |
| DELETE | `/api/v1/categories/{category_id}` | Delete a category     | Administrator |


### Orders

| Method | Endpoint                           | Description                                | Access     |
|--------|------------------------------------|--------------------------------------------|------------|
| GET    | `/api/v1/orders/`                  | Get orders available to the current user   | Authorized |
| GET    | `/api/v1/orders/{order_id}`        | Get a single order with its items          | Authorized |
| POST   | `/api/v1/orders/`                  | Create a new pending order                 | Authorized |
| POST   | `/api/v1/orders/{order_id}/items`  | Add a book to an existing pending order    | Authorized |
| POST   | `/api/v1/orders/{order_id}/cancel` | Cancel an eligible order and restore stock | Authorized |

## Request Examples

### Register
```http
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "Password123!"}'
```

### Login
```http
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=Password123!"
```

### Refresh Tokens
```http
curl -X POST "http://localhost:8000/api/v1/auth/refresh?refresh_token=<refresh-token>"
```

### Get Books
```http
curl http://localhost:8000/api/v1/books/
```

### Get Orders
```http
curl http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Bearer <access-token>"
```

### Create an Order
```http
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Bearer <access-token>"
```

### Add an Item to an Order
```http
curl -X POST http://localhost:8000/api/v1/orders/<order-uuid>/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access-token>" \
  -d '{"book_id": "<book-uuid>", "quantity": 2}'
``` 

### Get a Single Order
```http
curl http://localhost:8000/api/v1/orders/<order-uuid> \
  -H "Authorization: Bearer <access-token>"
```

### Cancel an Order
```http
curl -X POST http://localhost:8000/api/v1/orders/<order-uuid>/cancel \
  -H "Authorization: Bearer <access-token>"
```


## Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Start tests
pytest
```
> Warning: The integration tests clear the database after each test. Run the test suite only against a dedicated development/test database. Do not run it against a production database or any database containing important data.


## Environment Variables

| Variable                      | Description                        | Default                                                         |
|-------------------------------|------------------------------------|-----------------------------------------------------------------|
| `DATABASE_URL`                | Async PostgreSQL connection string | postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore |
| `SECRET_KEY`                  | Secret key used for JWT signing    | dev-secret-key                                                  |
| `ALGORITHM`                   | JWT signing algorithm              | HS256                                                           |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime              | 30                                                              |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Refresh token lifetime             | 7                                                               |

> Don't use the exact names defined in `.env.example`. Never commit real secrets or database credentials.

## Database Migrations

```bash
# Create new migrations
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show migrations history
alembic history

# Check the current revision
alembic current
```

> Alembic is configured to work with the application's asynchronous SQLAlchemy setup.


## Notes

### JWT Authentication

The API uses access and refresh tokens. A refresh endpoint allows clients to obtain a new token pair without repeating the login flow.

### Role-Based Access Control

Two roles are supported:

* `USER` — regular authenticated user
* `ADMIN` — administrator with access to management operations

### Order Creation Flow

1. Create an order.
2. Add one or more books to the order.
3. The server checks stock availability and updates the order total.
4. The order can then be cancelled if it is still in an eligible status.


### Book and Category Management

Books can be associated with multiple categories through the `book_categories` association table.

### Order Management

Orders start in `PENDING` status. The server controls status and calculated financial fields instead of allowing clients to modify them directly.

### Stock Control

Adding books to an order decreases stock. Cancelling an eligible order restores the reserved stock.

### Transaction-Safe Order Operations

Critical inventory operations use row-level locking to protect stock from conflicting concurrent updates.


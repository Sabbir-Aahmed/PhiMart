# PhiMart-E-Commercer-API

PhiMart is a full-featured e-commerce backend API built with Django REST Framework. It provides endpoints for managing products, categories, carts, and orders, with secure JWT-based authentication and comprehensive API documentation.

---

## Features

- **Product Management**: Create, retrieve, update, and delete products
- **Category Management**: Organize products by categories
- **Shopping Cart**: Add, update, and remove items from user carts
- **Order Processing**: Place and manage orders
- **JWT Authentication**: Secure user registration, login, and token management powered by [Djoser](https://github.com/sunscrapers/djoser)
- **API Documentation**: Interactive Swagger UI generated with [drf_yasg](https://github.com/axnsan12/drf-yasg)

---

## Tech Stack

- **Python**
- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **Djoser** - Authentication
- **drf_yasg** - API documentation (Swagger)
- **PostgreSQL / SQLite** - Database

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)
- PostgreSQL or SQLite (default)

### Installation

1.**Clone the repository**

```bash
git clone https://github.com/Sabbir-Aahmed/PhiMart.git
cd phimart
```
2.**Create and activate a virtual environment**

```
python -m venv venv
source venv/bin/activate   
# On Windows:venv\Scripts\activate
```
3.**Install dependencies**

```
pip install -r requirements.txt
```
4.**Configure environment variables**

Create a .env file or set environment variables as needed for:

 - DJANGO_SECRET_KEY

 - Database credentials (if using PostgreSQL)

 - Other settings as needed

5.**Apply migration**
```
python manage.py migrate
```
6.**Create a superuser**
```
python manage.py createsuperuser
```
7.**Run the development server**

```
python manage.py runserver
```

## API Endpoints

| Endpoint             | HTTP Methods              | Description                        |
|----------------------|---------------------------|----------------------------------|
| `/api/v1/products/`      | `GET`, `POST`             | List all products or create a new product |
| `/api/v1/products/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Retrieve, update, or delete a product by ID |
| `/api/v1/categories/`    | `GET`, `POST`             | List all categories or create a new category |
| `/api/v1/carts/`         | `GET`, `POST`             | View or add items to the shopping cart |
| `/api/v1/carts/{id}/`    | `PATCH`, `DELETE`         | Update or remove a cart item by ID |
| `/api/v1/orders/`        | `GET`, `POST`             | List all orders or place a new order |
| `/api/v1/orders/{id}/`   | `GET`, `PATCH`, `DELETE`  | Retrieve, update, or cancel an order |
| `/api/v1//auth/`              | `POST`                    | JWT Authentication endpoints (login, register, etc.) via Djoser |

---

### Example Request

```http
GET /api//v1/products/
Host: localhost:8000
Authorization: Bearer <your_access_token>
Accept: application/json
```

## API Documentation
The interactive Swagger UI is available at:
```
http://localhost:8000/swagger/
```

## Environment Variables

Create a `.env` file in your project root with the following variables:

```env
# Django settings
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL example)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=phimart_db
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

# JWT token lifetimes (optional)
JWT_ACCESS_TOKEN_LIFETIME=5m
JWT_REFRESH_TOKEN_LIFETIME=1d
```
## License
This project is licensed under the MIT License.

## Contact

Created by **Md Sabbir Ahmed**

- Email: [mdsabbir5820@gmail.com](mailto:mdsabbir5820@gmail.com)   
- LinkedIn: [https://www.linkedin.com/in/md-sabbir-ahmed/](https://www.linkedin.com/in/md-sabbir-ahmed/)  

Feel free to reach out for questions, suggestions, or collaboration!

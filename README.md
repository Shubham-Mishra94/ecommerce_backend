A robust Django + DRF-based backend system for an eCommerce platform with JWT authentication, real-time WebSocket-based order notifications, Redis caching, Postgres database, and API testing using Postman.
Project Structure
ecommerce_backend/               # Main Django project folder

├── ecommerce_backend/           # Project settings, ASGI/WSGI, urls

│   ├── settings.py              # All project configurations

│   ├── urls.py                  # Root URL dispatcher

│   └── asgi.py                  # ASGI setup for WebSocket support

├── core/                        # Django app for business logic

│   ├── __init__.py

│   ├── admin.py                 # Admin configurations

│   ├── apps.py                  # Core app config

│   ├── consumers.py             # WebSocket consumer for live order status

│   ├── filters.py               # DjangoFilter for product filtering

│   ├── models.py                # Models: User, Product, Category, Order

│   ├── notifications.py         # WebSocket broadcast helper

│   ├── routing.py               # WebSocket routing

│   ├── serializers.py           # DRF serializers

│   ├── signals.py               # Signal handlers (e.g. cache invalidation)

│   ├── urls.py                  # Core app URL router

│   ├── views.py                 # API endpoints using DRF ViewSets

│   └── migrations/

└── manage.py

Technologies Used

1. Backend: Django 4.x, Django REST Framework
2. Auth: JWT (SimpleJWT)
3. Database: PostgreSQL 17
4. Caching: Redis
5. Real-time: Django Channels
6. API Testing: Postman

Setup Instructions
1. Clone and Setup Virtual Env
     git clone <repo-url>
     cd ecommerce_backend
     python -m venv venv
     source venv/bin/activate  # Windows: venv\Scripts\activate
     pip install -r requirements.txt

2.PostgreSQL Setup
     Create a DB named ecommerce_db (or your choice).
     Update settings.py:
            DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
     
3. Redis Setup(Install Redis and start) using WSL: redis-server
4. Run Migrations
       python manage.py makemigrations
       python manage.py migrate
5. Create SuperUser
       python manage.py createsuperuser
6. Run Development server: python manage.py runserver
7. For Websockets: python manage.py runserver
8. API Testing using POSTMAN:
    1. Register:
                POST /api/register/
                Body:
                    {
                      "username": "testuser",
                      "password": "password123",
                      "email": "user@example.com"
                    }
     2. Obtain Token:   POST /api/token/
                        Body:
                            {
                              "username": "testuser",
                              "password": "password123"
                            }
     3. Authenticated Requests: Key: Authorization
                                Value: Bearer <access_token>

     4. CRUD API Endpoints:
                           GET /api/categories/
                           GET /api/products/
                           POST /api/products/ (admin only)
                           PUT /api/products/<id>/
                           DELETE /api/products/<id>/
                           POST /api/orders/ (create order)
                           PATCH /api/orders/<id>/ (admin update status)

9. Redis and Cache Testing:
Steps:
Call GET /api/products/ in Postman (data fetched from DB)
Call again (data fetched from Redis cache)
Check in Redis CLI:
                  redis-cli
                  KEYS *
                  TTL product_list
When a product is created/updated/deleted, cache is invalidated via signals.py.

10. Real-Time Notifications (WebSocket)
    WebSocket Endpoint: ws://127.0.0.1:8000/ws/orders/
    Steps:
         Login as user in Postman & create an order.
         Open WebSocket testing tool (e.g., piesocket.com)
         Connect to ws://127.0.0.1:8000/ws/orders/ using authenticated user.
         When order status is updated by admin, the WebSocket receives:
                                                                      {
                                                                         "order_id": 1,
                                                                         "new_status": "shipped"
                                                                       }


Summary of Features

-- JWT-based authentication & authorization
-- Product/category/order APIs with role-based access
-- Redis caching of product/category listing
-- Automatic cache invalidation using Django signals
-- Real-time order status updates with Django Channels + WebSocket
-- Structured modular app design (core app only)


FROM CODER :
          This backend is designed for scalable and extensible eCommerce development.
          If you need production deployment support AWS, Docker and GCP, feel free to reach out!








<a name="drf-react-gems"></a>

# 🛍️ DRF React Gems - E-commerce Platform

[![Django](https://img.shields.io/badge/Django-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-blue.svg)](https://reactjs.org/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT%20Authentication-gray.svg)](https://jwt.io/)
[![Azure](https://img.shields.io/badge/Azure-blue.svg)](https://azure.microsoft.com/)
[![Redis](https://img.shields.io/badge/Redis-red.svg)](https://redis.io/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-teal.svg)](https://cloudinary.com/)
[![Firebase](https://img.shields.io/badge/Firebase-orange.svg)](https://firebase.google.com/)
[![Sentry](https://img.shields.io/badge/Sentry-purple.svg)](https://sentry.io/)

A full-stack e-commerce platform built with Django REST Framework (DRF) backend and React frontend. Implements user authentication, shopping cart and wishlist functionality, payment processing, order history and asynchronous email notifications using Celery and Redis.

**Live Application: [https://drf-react-gems.web.app](https://drf-react-gems.web.app/)**

**Admin Panel: [https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin](https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin)**

**API documentation: [https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net](https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net)**

<p align="center">
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.45.11_e0m7vo.png" width="260" />
  &nbsp;
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.50.53_opvgpj.png" width="260"/>
  &nbsp;
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.54.43_cfyql5.png" width="260"/>
  &nbsp;
</p>

## 📋 Table of Contents

### 1. Key Features

-   [Django Framework Implementation](#django-framework-implementation)
-   [Database Service](#database-service)
-   [Frontend Implementation](#frontend-implementation)
-   [Authentication Functionality](#authentication-functionality)
-   [Password Reset System](#password-reset-system)
-   [Access Control](#access-control)
-   [Customized Admin Site](#customized-admin-site)
-   [Admin Groups](#admin-groups)
-   [Exception Handling and Data Validation](#exception-handling-and-data-validation)
-   [Asynchronous Processing](#asynchronous-processing)
-   [Testing](#testing)
-   [Deployment](#deployment)
-   [Django User Extension](#django-user-extension)
-   [Object-Oriented Design](#object-oriented-design)

### 2. Quick Start

-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Database Population](#database-population)

---

## 1. Key Features

### Django Framework Implementation

-   Complete Django configuration with DRF, JWT, CORS, and database settings: [server/src/settings.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/settings.py)

-   [The application has 16 independent class-based views](https://github.com/beatrisilieva/drf-react-gems/blob/main/docs/views.md)

-   [The application has 12 independent models](https://github.com/beatrisilieva/drf-react-gems/blob/main/docs/models.md)

-   [The application has 7 forms (implemented with DRF serializers and React components)](https://github.com/beatrisilieva/drf-react-gems/blob/main/docs/forms.md)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Database Service

-   **PostgreSQL database is used as the primary database**

-   **Data Normalization:** The database is organized to avoid repeating the same data in different places. It follows the main rules of database design:

    -   **First Normal Form (1NF):** Each table has columns that hold just one piece of information (no lists or groups in a single cell). For example, the `products_color` table has a column for the color name, and each row is a single color
    -   **Second Normal Form (2NF):** All details in a table are linked only to that table's main ID. For example, in the `products_inventory` table, the amount in stock and the price are linked to a specific product and size
    -   **Third Normal Form (3NF):** There are no “hidden” connections between details. For example, product features like color, metal, and stone are always stored in their own tables and linked by ID

-   **Entity Relationship Diagram:**

![ERD](https://res.cloudinary.com/dpgvbozrb/image/upload/v1752592187/ERD.pgerd_w6i0a3.png)

-   **Cloudinary is used to store user profile photos:**

    -   UserPhoto: [server/src/accounts/models/user_photo.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/models/user_photo.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Frontend Implementation

-   [The application has 14 page components](https://github.com/beatrisilieva/drf-react-gems/blob/main/docs/web_pages.md)

-   **Web Page Design:** Custom SCSS modules for component-based styling, ensuring modularity

-   **User Interface:** Fully responsive UI, adapting to various screen sizes with reusable React components

-   **User Experience:** Accessible navigation and consistent interactive elements (buttons, forms, popups)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Authentication Functionality

-   JWT-based authentication system for login, registration, logout, and account deletion via `UserRegisterView`, `UserLoginView`, `UserLogoutView`, and `UserDeleteView`

-   Custom authentication backend allowing users to authenticate using either email or username through [CustomAuthBackendBackend](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/authentication.py)

-   Password change functionality, handled by `UserPasswordChangeView`

    [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Password Reset System

-   **Two-step password reset process:** Users request reset via email, then confirm with token-based validation
-   **Token-based verification:** Uses Django's built-in token generator with URL-safe base64 encoding for user identification
-   **Email delivery:** Automated password reset emails sent via Gmail SMTP with HTML templates
-   **Validation:** Confirms token validity, password strength requirements, and password confirmation matching
-   **Implementation:** Handled by `UserPasswordResetRequestView` and `UserPasswordResetConfirmView`

    [server/src/accounts/serializers/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Access Control

-   **Public Access:** Anonymous users can browse products and use a guest shopping cart/wishlist stored in `Local Storage`

-   **Private Access:** Authenticated users access checkout, account management, order history, and permanent storage of shopping bag/wishlist. Admin page access is restricted to Order group admins for sending abandoned cart reminders

-   **Review Moderation:** Regular users see only approved reviews; Order group users (with `products.approve_review` permission) view all reviews

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Customized Admin Site

-   **Custom Django admin with Unfold framework:**

    -   Unfold Framework: Admin interface with custom themes, and styling [server/src/unfold.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/unfold.py)
    -   Custom Navigation: Organized sidebar with collapsible sections for Users & Groups, Products, Product Attributes, and Reviews
    -   Permission-Based Access: Different admin sections visible based on user permissions

-   **The admin interface includes 5 custom options:**

    -   List filters (e.g., by stone and color)
    -   List display with image previews
    -   Ordering of records
    -   Search fields for product attributes
    -   Inline editing of related inventory

    See implementation: [server/src/products/admin.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/admin.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Admin Groups

**3 admin groups with different permission levels are implemented:**

-   **Superuser:**

    -   Complete system administration with all CRUD operations
    -   Full access to all admin sections including Users & Groups

-   **Inventory Group:**

    -   Full CRUD access to products, inventory, and attributes
    -   Access to Products and Product Attributes sections

-   **Order Group:**

    -   Can approve, and disapprove customer reviews for products they have purchased
    -   Access to Product Reviews section

**Automated Setup:**

All admin groups and their associated users are created automatically by a management command: [server/src/accounts/management/commands/create_roles.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/management/commands/create_roles.py)

| User Type      | Email                     | Password |
| -------------- | ------------------------- | -------- |
| Super User     | `super_user@mail.com`     | `!1Aabb` |
| Inventory User | `inventory_user@mail.com` | `!1Aabb` |
| Order User     | `order_user@mail.com`     | `!1Aabb` |

**To access the Admin Panel visit: [https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin](https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin)**

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Exception Handling and Data Validation

-   **Server-side:**

    -   Error handling is implemented using try-except blocks and DRF exception classes, particularly for authentication and business-critical operations
    -   Password validation: [server/src/accounts/validators/password.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/validators/password.py)
    -   Payment & order validation: [server/src/orders/services.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/services.py)
    -   Model validation: [server/src/accounts/validators/model.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/validators/models.py)

-   **Client-side:**

    -   Real-time form validation: All forms (registration, login, delivery, payment, password update, etc.) provide instant feedback as users type, using custom React hooks and validation helpers, preventing invalid requests to backend
    -   Visual feedback: Input fields dynamically change color to indicate validation state (green for valid, red for invalid, blue for focus)
    -   Server-side error integration: Any validation errors returned from the backend are mapped to the correct form fields and displayed to the user in real time

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Asynchronous Processing

-   **Asynchronous Views:**

    -   `notify_users_they_have_uncompleted_orders` allows Order group admins to send reminder emails for shopping bags older than one day: [server/src/common/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/common/views.py)

        -   **Demo:** Access the admin notification page at `https://drf-react-gems.web.app/admin-page` (requires authentication with Order User credentials: `order_user@mail.com` / `!1Aabb`)

    -   `send_email` handles email notifications via Gmail SMTP using Google App Password authentication: [server/src/common/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/common/views.py)

-   **Background Tasks powered by Celery with Redis:**

    -   User greeting emails sent on registration: [server/src/accounts/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/signals.py)

    -   Scheduled task to mark old orders as completed: [server/src/orders/tasks.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/tasks.py)

    -   Review approval notification emails: [server/src/products/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/signals.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Testing

-   **66 Unit & Integration tests with [74% coverage report](https://beatrisilieva.github.io/drf-react-gems/coverage-report/index.html)**

    (`coverage run manage.py test && coverage report`)

    [![Coverage](https://img.shields.io/badge/coverage-74%25-green.svg)](https://beatrisilieva.github.io/drf-react-gems/coverage-report/index.html)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Deployment

-   **Backend**: `Azure` and `Redis Cloud`

-   **Frontend**: `Firebase`

-   **Coverage Report**: `GitHub Pages`

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Django User Extension

-   **Custom user model:** Uses email as the primary login identifier, with unique username and additional fields for marketing consent

-   **User profile:** Stores personal and shipping information in a dedicated profile model linked one-to-one with the user

-   **User photo:** Handles user profile pictures with cloud storage

-   **Automatic profile and photo creation using signals:** When a UserCredential is created, Django signals automatically create corresponding UserProfile and UserPhoto database objects with the same primary key as the UserCredential model, establishing one-to-one relationships [server/src/accounts/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/signals.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Object-Oriented Design

-   **Inheritance:** All product categories inherit from an abstract base product model, allowing shared fields [server/src/products/models/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/base.py)

-   **Open/Closed Principle:** New categories with own fields extend existing logic by adding new models without modification [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)

-   **Polymorphic Relations:** Instead of separate inventory and review models per product type, inventory [server/src/products/models/inventory.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py) and review [server/src/products/models/review.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/review.py) models use Django’s `GenericForeignKey` to relate to any product category. In the inventory model, each product is represented in three sizes, with each size having its own price and quantity. Combined with generic relations, this design enables a single inventory and review system shared across all product categories

-   **Abstraction:** Product fetching logic is abstracted into `BaseProductManager`, keeping query details hidden from the views. The manager handles `prefetch_related` for inventory and review relations, `values` to retrieve base product fields, and annotations with `Min`, `Max`, and `Avg` to provide price ranges and average rating per product

-   **Data encapsulation:** Business logic and data validation are encapsulated within dedicated service classes and model managers

-   **Cohesion and loose coupling:** Each Django app (accounts, products, orders, shopping_bags and wishlists) encapsulates a distinct business domain. Django apps are primarily independent from each other

-   **Code quality and readability:** All code adheres to PEP 8 (Python) and uses ESLint/Prettier (JavaScript) for consistent formatting

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

---

## 2. Quick Start

### Prerequisites

-   Python

-   Node.js

-   PostgreSQL

-   Redis

-   Git

### Installation

#### 1. Clone and setup

```bash
git clone https://github.com/BeatrisIlieva/drf-react-gems.git
cd drf-react-gems
```

---

#### 2. Backend environment variables

-   Create `.env` in the `server/` directory:

```bash
cd server
touch .env
```

-   Example settings for LOCAL DEVELOPMENT ONLY

```env
# Django Configuration
SECRET_KEY=your-secret-key                         # REQUIRED: Generate new Django secret key

# Local Development URLs
ALLOWED_HOSTS=localhost,127.0.0.1                  # OK for local
CORS_ALLOWED_ORIGINS=http://localhost:5173         # OK for local
CSRF_TRUSTED_ORIGINS=http://localhost:5173         # OK for local
FRONTEND_URL=http://localhost:5173                 # OK for local; Needed for password reset

# Database (PostgreSQL)
DB_NAME=your_database_name                         # REQUIRED: Your PostgreSQL database name
DB_USER=your_username                              # REQUIRED: Your PostgreSQL username
DB_PASS=your_password                              # REQUIRED: Your PostgreSQL password
DB_HOST=127.0.0.1                                  # OK for local
DB_PORT=5432                                       # OK for local

# Cloudinary (Media Storage)
CLOUD_NAME=your_cloud_name                         # REQUIRED: From your Cloudinary account
CLOUD_API_KEY=your_api_key                         # REQUIRED: From your Cloudinary account
CLOUD_API_SECRET=your_api_secret                   # REQUIRED: From your Cloudinary account

# Redis (Celery)
CELERY_BROKER_URL=redis://localhost:6379/0         # OK for local
CELERY_RESULT_BACKEND=redis://localhost:6379/0     # OK for local

# Email Service
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email@example.com
DEFAULT_FROM_EMAIL=your_email@example.com
SERVER_EMAIL=your_email@example.com
EMAIL_HOST_PASSWORD=your-SMTP-app-password         # REQUIRED: Generate app password in your
                                                   # Google Account settings

# Sentry (Error Monitoring)
SENTRY_DSN=your_sentry_dsn                         # REQUIRED: From your Sentry project dashboard
                                                   # Set to empty string if not using:
                                                   # SENTRY_DSN=

DEBUG=True                                         # OK for local
```

---

#### 3. Backend setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Populate database with products, reviews, and roles
python manage.py setup_database
```

---

**Use `honcho` to run all processes defined in the [Procfile]**(https://github.com/beatrisilieva/drf-react-gems/blob/main/server/Procfile):

---

```bash
# Start the backend server
export PORT=8000 && honcho start
```

---

#### 4. Frontend environment variables

-   Create `.env` in the `client/` directory:

```bash
cd client
touch .env.development
```

-   Example settings for LOCAL DEVELOPMENT ONLY

```env.development
VITE_APP_SERVER_URL=http://localhost:8000
```

---

#### 5. Frontend setup

```bash
cd client
npm install
npm run dev
```

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Database Population

The `python manage.py setup_database` command (run during installation) will:

-   Create all products with categories, collections, colors, metals, stones and inventories
-   Add customer reviews with ratings and comments
-   Create admin users with different roles and permissions
-   Create a superuser with full system access

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## License

This project is licensed under the MIT License.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

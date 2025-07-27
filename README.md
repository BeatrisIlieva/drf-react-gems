<a name="drf-react-gems"></a>

# 🛍️ DRF React Gems - E-commerce Platform

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.14+-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT%20Authentication-green.svg)](https://jwt.io/)
[![Azure](https://img.shields.io/badge/Azure-blue.svg)](https://azure.microsoft.com/)
[![Redis](https://img.shields.io/badge/Redis-6+-red.svg)](https://redis.io/)
[![Firebase](https://img.shields.io/badge/Firebase-orange.svg)](https://firebase.google.com/)

A full-stack e-commerce platform built with Django REST Framework (DRF) backend and React frontend. Features user authentication, shopping cart and wishlist functionality, secure payment processing, order history and asynchronous email notifications using Celery and Redis.

**Live Application: [https://drf-react-gems.web.app](https://drf-react-gems.web.app/)**

**Admin Panel: [https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin](https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin)**

<p align="center">
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.45.11_e0m7vo.png" width="260" />
  &nbsp;
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.50.53_opvgpj.png" width="260"/>
  &nbsp;
  <img src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1752676884/Screenshot_2025-07-15_at_20.54.43_cfyql5.png" width="260"/>
  &nbsp;
</p>

## 📋 Table of Contents

### 1. General Requirements

-   [Django Framework Implementation](#django-framework-implementation)
-   [Database Service](#database-service)
-   [Frontend Implementation](#frontend-implementation)
-   [Web Page Design](#web-page-design)
-   [Authentication Functionality](#authentication-functionality)
-   [Public Part](#public-part)
-   [Private Part](#private-part)
-   [Customized Admin Site](#customized-admin-site)
-   [Admin Groups](#admin-groups)
-   [Exception Handling and Data Validation](#exception-handling-and-data-validation)

### 2. Bonus Features

-   [Testing Implementation](#testing-implementation)
-   [Asynchronous Views](#asynchronous-views)
-   [Background Tasks with Celery and Redis](#background-tasks-with-celery-and-redis)
-   [REST API Implementation](#rest-api-implementation)
-   [Django User Extension](#django-user-extension)
-   [Deployment](#deployment)
-   [Additional Functionality](#additional-functionality)

### 3. Additional Requirements

-   [Object-Oriented Design](#object-oriented-design)
-   [User Interface](#user-interface)
-   [User Experience](#user-experience)

### 4. Quick Start

-   [Installation](#installation)
-   [Database Population](#database-population)

---

## 1. General Requirements

### Django Framework Implementation

**The application is implemented using Django Framework:**

-   Complete Django configuration with DRF, JWT, CORS, and database settings [server/src/settings.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/settings.py)

**The application has 13 page components:**

-   Home page [client/src/components/pages/home/Home.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/home/Home.jsx)
-   Product list page [client/src/components/pages/product-list/ProductList.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/product-list/ProductList.jsx)
-   Product item page [client/src/components/pages/product-item/ProductItem.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/product-item/ProductItem.jsx)
-   Shopping bag page [client/src/components/pages/shopping-bag/ShoppingBag.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/shopping-bag/ShoppingBag.jsx)
-   Wishlist page [client/src/components/pages/wishlist/Wishlist.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/wishlist/Wishlist.jsx)
-   Checkout page [client/src/components/pages/checkout/Checkout.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/checkout/Checkout.jsx)
-   Payment page [client/src/components/pages/payment/Payment.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/payment/Payment.jsx)
-   Order confirmation page [client/src/components/pages/order-confirmation/OrderConfirmation.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/order-confirmation/OrderConfirmation.jsx)
-   Login page [client/src/components/pages/login/Login.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/login/Login.jsx)
-   Register page [client/src/components/pages/register/Register.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/register/Register.jsx)
-   Accounts page [client/src/components/pages/accounts/Accounts.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/accounts/Accounts.jsx)
-   Admin page [client/src/components/pages/admin/Admin.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/admin/Admin.jsx)
-   404 page [client/src/components/pages/page404/Page404.jsx](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/page404/Page404.jsx])

**The application has 14 independent class-based views:**

-   BaseProductListView [server/src/products/views/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   BaseProductItemView [server/src/products/views/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   BaseAttributeView [server/src/products/views/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   OrderViewSet [server/src/orders/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/views.py)
-   ShoppingBagViewSet [server/src/shopping_bags/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/shopping_bags/views.py)
-   WishlistViewSet [server/src/wishlists/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/wishlists/views.py)
-   ReviewViewSet [server/src/products/views/review.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/review.py)
-   UserRegisterView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserLoginView [server/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserLogoutView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   PasswordChangeView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserDeleteView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserProfileView [server/src/accounts/views/user_profile.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_profile.py)
-   PhotoUploadView [server/src/accounts/views/user_photo.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_photo.py)

**The application has 12 independent models:**

-   UserCredential [server/src/accounts/models/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/models/user_credential.py)
-   Order [server/src/orders/models.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/models.py)
-   BaseProduct [server/src/products/models/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/base.py)
-   Collection [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   Color [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   Metal [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   Stone [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   Inventory [server/src/products/models/inventory.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py)
-   Size [server/src/products/models/inventory.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py)
-   Review [server/src/products/models/review.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/review.py)
-   ShoppingBag [server/src/shopping_bags/models.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/shopping_bags/models.py)
-   Wishlist [server/src/wishlists/models.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/wishlists/models.py)

**The application has 6 forms (implemented with DRF serializers and React components):**

-   User registration form [server/src/accounts/serializers/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   User login form [server/src/accounts/serializers/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   Password change form [server/src/accounts/serializers/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   Delivery information form [server/src/accounts/serializers/user_profile.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_profile.py)
-   Payment form [server/src/orders/serializers.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/serializers.py)
-   Product review form [server/src/products/serializers/review.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/serializers/review.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Database Service

**PostgreSQL database is used as the primary database:**

-   Database configuration with PostgreSQL 13+

**Data Normalization:** The database is organized to avoid repeating the same data in different places. It follows the main rules of database design:

-   **First Normal Form (1NF):** Each table has columns that hold just one piece of information (no lists or groups in a single cell). For example, the `products_color` table has a column for the color name, and each row is a single color
-   **Second Normal Form (2NF):** All details in a table are linked only to that table's main ID. For example, in the `products_inventory` table, the amount in stock and the price are linked to a specific product and size
-   **Third Normal Form (3NF):** There are no “hidden” connections between details. For example, product features like color, metal, and stone are always stored in their own tables and linked by ID

**Entity Relationship Diagram:**

![ERD](https://res.cloudinary.com/dpgvbozrb/image/upload/v1752592187/ERD.pgerd_w6i0a3.png)

**Cloudinary is used to store user profile photos:**

-   UserPhoto: [server/src/accounts/models/user_photo.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/models/user_photo.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Frontend Implementation

-   React-based Single Page Application (SPA)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Web Page Design

-   Custom SCSS modules for component-based styling

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Authentication Functionality

**The application has login/register/logout/delete account functionality:**

-   Complete JWT-based authentication system
-   UserRegisterView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserLoginView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserLogoutView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   UserDeleteView [server/src/accounts/views/user_credential.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Public Part

**Public part is accessible by everyone:**

-   Anonymous users can browse products and use guest shopping cart/wishlist

> **Note:**  
> Guest users can add, remove, and update items in their shopping bag and wishlist, with each guest’s data kept in `Local Storage`. When a guest registers or logs in, their shopping bag and wishlist are merged into their account.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Private Part

**The private part of the application is accessible only to authenticated users and admins:**

-   Access to checkout, account management, order history, and permanent storage of shopping bag and wishlist requires authentication

-   Access to the Admin page is available only to admins in the Order group. From there, they can send reminders to users about their abandoned shopping bags

**Review Moderation & Approval System:**

-   **Regular users** can only see reviews that have been approved on a product item page
-   **Order users** (users in the "order" group with the `products.approve_review` permission) can see all reviews (approved and unapproved) for a product

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Customized Admin Site

**Custom Django admin with Unfold framework:**

-   Unfold Framework: Admin interface with custom themes, and styling [server/src/unfold.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/unfold.py)
-   Custom Navigation: Organized sidebar with collapsible sections for Users & Groups, Products, Product Attributes, and Reviews
-   Permission-Based Access: Different admin sections visible based on user permissions

**To access the Admin Panel visit: [https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin](https://drf-react-gems-f6escmbga4gkbgeu.italynorth-01.azurewebsites.net/admin)**

**The admin interface includes 5 custom options:**

-   List filters (e.g., by stone and color)
-   List display with image previews
-   Ordering of records
-   Search fields for product attributes
-   Inline editing of related inventory

See implementation: [server/src/products/admin.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/admin.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Admin Groups

**3 admin groups with different permission levels are implemented:**

#### **Superuser:**

-   Complete system administration with all CRUD operations
-   Full access to all admin sections including Users & Groups

#### **Inventory Group:**

-   Full CRUD access to products, inventory, and attributes
-   Access to Products and Product Attributes sections

#### **Order Group:**

-   Can approve, and disapprove customer reviews for products they have purchased
-   Access to Product Reviews section

##### **Automated Setup:**

-   All admin groups and their associated users are created automatically by a management command: [server/src/accounts/management/commands/create_roles.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/management/commands/create_roles.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Exception Handling and Data Validation

-   **Server-side:**

    -   Password validation: [server/src/accounts/validators/password.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/validators/password.py)
    -   Payment & order validation: [server/src/orders/services.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/services.py)
    -   Model validation: [server/src/accounts/validators/model.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/validators/models.py)

-   **Client-side:**
    -   Real-time form validation: All forms (registration, login, delivery, payment, password update, etc.) provide instant feedback as users type, using custom React hooks and validation helpers
    -   Visual feedback: Input fields dynamically change color to indicate validation state (green for valid, red for invalid, blue for focus)
    -   Server-side error integration: Any validation errors returned from the backend are mapped to the correct form fields and displayed to the user in real time

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## 2. Bonus Features

### Testing Implementation

**The project includes 60 automated tests.**

-   Shows 84% coverage (`coverage run manage.py test && coverage report`)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Asynchronous View

**Shopping Bag Reminder System:**

-   An asynchronous view `notify_users_they_have_uncompleted_orders` allows Order group admins to send reminder emails for shopping bags older than one day. This function is triggered by a button on the admin page within the web application (not the admin interface), requiring Order group permissions after login. Implemented with Celery: [server/src/common/views.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/common/views.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Background Tasks with Celery and Redis

-   **User Greeting Email:** Sent asynchronously on registration: [server/src/accounts/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/signals.py)
-   **Order Completion:** Scheduled task marks old orders as completed: [server/src/orders/tasks.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/tasks.py)
-   **Review Approval Notification:** Emails sent on review approval: [server/src/products/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/signals.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### REST API Implementation

-   The backend utilizes DRF API views and serializers to provide all features to the React frontend

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Django User Extension

-   **Custom user model:** Uses email as the primary login identifier, with unique username and additional fields for marketing consent

-   **User profile:** Stores personal and shipping information in a dedicated profile model linked one-to-one with the user

-   **User photo:** Handles user profile pictures with cloud storage

-   **Automatic profile and photo creation using signals:** When a UserCredential is created, Django signals automatically create corresponding UserProfile and UserPhoto database objects with the same primary key as the UserCredential model, establishing one-to-one relationships [server/src/accounts/signals.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/signals.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Deployment

-   **Backend:** Deployed on Azure with Redis Cloud for background tasks
-   **Frontend:** Deployed on Firebase

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## 3. Additional Requirements

### Object-Oriented Design

-   **Data encapsulation:** Business logic and data validation are encapsulated within dedicated service classes and model managers

-   **Exception handling:** Error handling is implemented using try-except blocks and DRF exception classes, particularly for authentication and business-critical operations

-   **Inheritance, abstraction, and polymorphism:** All product categories inherit from an abstract base product model [server/src/products/models/base.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/base.py), allowing shared fields. Instead of creating separate inventory and review models for each product type, the inventory [server/src/products/models/inventory.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py) and review [server/src/products/models/review.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/review.py) models use Django’s GenericForeignKey to relate to any product category. This design enables a single inventory and review system for all product types defined in [server/src/products/models/product.py](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py).

    > **Design rationale:**  
    > `GenericForeignKey` allows us to have dedicated models for each product category (Earwear, Neckwear, etc.), so the backend can query and manage each category without filtering a single large product table.

-   **Cohesion and loose coupling:** Each Django app (accounts, products, orders, shopping_bags and wishlists) encapsulates a distinct business domain. Django apps are primarily independent from each other

-   **Code quality and readability:** All code adheres to PEP 8 (Python) and uses ESLint/Prettier (JavaScript) for consistent formatting

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### User Interface

-   **Responsive design:** The UI is fully responsive, adapting to different screen sizes and devices

-   **Component-based architecture:** The frontend is built with reusable, modular React components

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### User Experience

-   **Accessible and intuitive navigation:** The application uses clear navigation patterns and accessible controls

-   **Consistent user experience:** All interactive elements, from buttons to forms and popups, follow a unified style and behavior

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

---

## 4. Quick Start

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
DEBUG=True                                         # OK for local

# Local Development URLs
ALLOWED_HOSTS=localhost,127.0.0.1                  # OK for local
CORS_ALLOWED_ORIGINS=http://localhost:5173         # OK for local
CSRF_TRUSTED_ORIGINS=http://localhost:5173         # OK for local

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
EMAIL_HOST_PASSWORD=your-SMTP-app-password         # REQUIRED: Generate app password in your
                                                   # Google Account settings
```

---

#### 3. Backend setup

**Prerequisites:**

-   Make sure you have PostgreSQL installed and running
-   Create a PostgreSQL database (use any method you prefer: pgAdmin, command line, etc.)
-   Update your .env file with your database name, username, and password
-   Make sure you have Redis available (use any method you prefer: Docker, Redis Cloud, etc.)

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

**Created Admin Users:**

| User Type | Email | Password |
|-----------|-------|----------|
| Super User | `super_user@mail.com` | `!1Aabb` |
| Inventory User | `inventory_user@mail.com` | `!1Aabb` |
| Order User | `order_user@mail.com` | `!1Aabb` |


<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## License

This project is licensed under the MIT License.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

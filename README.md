<a name="drf-react-gems"></a>

# 🛍️ DRF React Gems - E-commerce Platform

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.14+-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT%20Authentication-green.svg)](https://jwt.io/)
[![Azure](https://img.shields.io/badge/Azure%20Deployment-blue.svg)](https://azure.microsoft.com/)

A full-stack e-commerce platform built with Django REST Framework (DRF) backend and React frontend. Features user authentication, product management, shopping cart functionality, wishlist system, and secure payment processing.

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
-   [REST API Implementation](#rest-api-implementation)
-   [Django User Extension](#django-user-extension)
-   [Deployment](#deployment)
-   [Additional Functionality](#additional-functionality)

### 3. Additional Requirements

-   [Object-Oriented Design](#object-oriented-design)
-   [User Interface](#user-interface)
-   [User Experience](#user-experience)
-   [Source Control System](#source-control-system)

### 4. Quick Start

-   [Installation](#installation)
-   [Database Population](#database-population)

---

## 1. General Requirements

### Django Framework Implementation

**The application is implemented using Django Framework:**

-   Complete Django configuration with DRF, JWT, CORS, and database settings (`server/src/settings.py`)

**The application has 11 page components:**

-   [Home page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/home/Home.jsx)
-   [Product list page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/product-list/ProductList.jsx)
-   [Product item page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/product-item/ProductItem.jsx)
-   [Shopping bag page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/shopping-bag/ShoppingBag.jsx)
-   [Wishlist page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/wishlist/Wishlist.jsx)
-   [Checkout page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/checkout/Checkout.jsx)
-   [Payment page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/payment/Payment.jsx)
-   [Order confirmation page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/order-confirmation/OrderConfirmation.jsx)
-   [Login page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/login/Login.jsx)
-   [Register page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/register/Register.jsx)
-   [Accounts page](https://github.com/beatrisilieva/drf-react-gems/blob/main/client/src/components/pages/accounts/Accounts.jsx)

**The application has 15 independent class-based views:**

-   [BaseProductListView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   [BaseProductItemView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   [BaseAttributeView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   [AsyncBaseAttributeView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)
-   [OrderViewSet](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/views.py)
-   [ShoppingBagViewSet](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/shopping_bags/views.py)
-   [WishlistViewSet](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/wishlists/views.py)
-   [ReviewViewSet](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/review.py)
-   [UserRegisterView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserLoginView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserLogoutView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [PasswordChangeView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserDeleteView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserProfileView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_profile.py)
-   [PhotoUploadView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_photo.py)

**The application has 12 independent models:**

-   [UserCredential](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/models/user_credential.py)
-   [Order](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/models.py)
-   [BaseProduct](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/base.py)
-   [Collection](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   [Color](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   [Metal](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   [Stone](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/product.py)
-   [Inventory](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py)
-   [Size](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/inventory.py)
-   [Review](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/models/review.py)
-   [ShoppingBag](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/shopping_bags/models.py)
-   [Wishlist](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/wishlists/models.py)

**The application has 6 forms (implemented with DRF serializers and React components):**

-   [User registration form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   [User login form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   [Password change form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_credential.py)
-   [Product review form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/serializers/review.py)
-   [Delivery information form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/serializers/user_profile.py)
-   [Payment form](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/serializers.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Database Service

**PostgreSQL database is used as the primary database:**

-   Database configuration with PostgreSQL 13+

**Data Normalization:** The database is organized to keep information tidy and avoid repeating the same data in different places. It follows the main rules of database design:

-   **First Normal Form (1NF):** Each table has columns that hold just one piece of information (no lists or groups in a single cell). For example, the `products_color` table has a column for the color name, and each row is a single color.
-   **Second Normal Form (2NF):** All details in a table are linked only to that table's main ID. For example, in the `products_inventory` table, the amount in stock and the price are linked to a specific product and size, so there’s no confusion or extra copies.
-   **Third Normal Form (3NF):** There are no “hidden” connections between details. For example, product features like color, metal, and stone are always stored in their own tables and linked by ID, so if we change a color’s name, it updates everywhere at once.

**Entity Relationship Diagram:**

![ERD](https://res.cloudinary.com/dpgvbozrb/image/upload/v1752592187/ERD.pgerd_w6i0a3.png)

**Multiple storage systems are utilized:**

-   Cloudinary: [User profile photos are stored in Cloudinary](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/models/user_photo.py)

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
-   [UserRegisterView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserLoginView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserLogoutView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)
-   [UserDeleteView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/views/user_credential.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Public Part

**Public part is accessible by everyone:**

-   Anonymous users can browse products and use guest shopping cart/wishlist

> **Note:**  
> Guest users can add items to their shopping bag and wishlist, with each guest’s data isolated using a unique guest ID. All modifications—adding, removing, or updating items—are performed via API requests to the backend, which centrally enforces inventory validation and business rules. The frontend uses quantity information from the backend to prevent users from adding more items than are available or removing more than they have in their bag. When a guest registers or logs in, their shopping bag and wishlist are migrated to their new account, with checks to prevent duplicate items.
>
> This approach ensures data integrity, a smooth user experience, and prevents errors related to unavailable inventory.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Private Part

**The private part of the application is accessible only to authenticated users and admins:**

-   Access to checkout, account management, and order history requires authentication.

**Review Moderation & Approval System:**

-   **Regular users** can only see reviews that have been approved on a product item page
-   **Reviewers** (users in the "reviewer" group with the `products.approve_review` permission) can see all reviews (approved and unapproved) for a product
-   **Backend**: A dedicated DRF endpoint `/api/products/<category>/<pk>/all-reviews/` returns all reviews for a product, accessible only to reviewers
-   **Frontend**: The UI conditionally fetches and displays all reviews for reviewers, and only approved reviews for regular users. Approve/unapprove buttons are visible only to reviewers

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Customized Admin Site

**Custom Django admin with Unfold framework:**

-   Unfold Framework: [Admin interface with custom themes, and styling](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/unfold.py)
-   Custom Navigation: Organized sidebar with collapsible sections for Users & Groups, Products, Product Attributes, and Reviews
-   Permission-Based Access: Different admin sections visible based on user permissions

**The admin interface includes more than 5 custom options:**

-   Custom list filters (e.g., by stone and color)
-   Custom list display with image previews
-   Custom ordering of records
-   Custom search fields for product attributes
-   Custom fieldsets for organized editing
-   Inline editing of related inventory
-   Readonly and editable fields for reviews
-   Custom admin methods (e.g., product links)
-   Custom permissions for review moderation

[See implementation](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/admin.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Admin Groups

**3 admin groups with different permission levels are implemented:**

#### **Superuser (Full CRUD Access):**

-   Complete system administration with all CRUD operations
-   Full access to all admin sections including Users & Groups

#### **Inventory Group (Product Management):**

-   Full CRUD access to products, inventory, and attributes
-   Access to Products and Product Attributes sections

#### **Reviewer Group (Review Moderation):**

-   Can approve, and disapprove customer reviews for products they have purchased.
-   Access to Product Reviews section

**User roles are managed from the admin site:**

-   Django admin interface for role management

**Role management is secure and error-safe:**

-   Proper permission checks and error handling

**Automated Setup:**

-   [All admin groups and their associated users are created automatically by a management command ](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/management/commands/create_roles.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Exception Handling and Data Validation

**Comprehensive exception handling and data validation is implemented:**

-   **Server-side:**

    -   Password validation: [All password changes and registrations are validated using custom logic to enforce strong password policies.](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/validators/password.py)
    -   Payment & order validation: [All payment details (card number, expiry, CVV, cardholder name) are validated using regex and business rules before processing orders.](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/orders/services.py)
    -   Model & serializer validation: All user input is validated at the serializer and model level, ensuring only valid data is saved to the database.

-   **Client-side:**
    -   Real-time form validation: All forms (registration, login, delivery, payment, password update, etc.) provide instant feedback as users type, using custom React hooks and validation helpers.
    -   Visual feedback with green/red/blue states: Input fields dynamically change color to indicate validation state (green for valid, red for invalid, blue for focus).
    -   Server-side error integration: Any validation errors returned from the backend are mapped to the correct form fields and displayed to the user in real time.

## 2. Bonus Features

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Testing Implementation

**The project includes around 80 automated tests.**

-   Shows 80%+ coverage (`coverage run manage.py test && coverage report`)
-   Runs all tests (`python manage.py test`)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Asynchronous Views

**Asynchronous views are implemented to optimize user experience and server efficiency for product attribute filtering.**

-   Asynchronous endpoints allow the backend to handle multiple filter and product data requests concurrently, reducing wait times for users.
-   Implementation example: [AsyncBaseAttributeView](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/products/views/base.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### REST API Implementation

-   The backend utilizes DRF API views and serializers to provide all features to the React frontend, rather than using Django’s traditional HTML templates.
-   All business logic—including authentication, products, shopping bag, wishlist, orders, and reviews—is exposed through RESTful API endpoints.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Django User Extension

-   **Custom user model:** Uses email as the primary login identifier, with unique username and additional fields for marketing consent.

-   **User profile:** Stores personal and shipping information in a dedicated profile model linked one-to-one with the user.

-   **User photo:** Handles user profile pictures with cloud storage and automatic optimization.

-   **Automatic profile and photo creation:** [Django signals ensure that every new user automatically gets a profile and photo record.](https://github.com/beatrisilieva/drf-react-gems/blob/main/server/src/accounts/signals.py)

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Deployment

-   Azure App Service deployment is implemented

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Additional Functionality

-   **Polymorphic product relationships:**
    The products app uses Django's `GenericForeignKey` and `GenericRelation` to enable flexible, polymorphic relationships between products, inventory, and reviews.
    -   In `base.py`, all product types inherit from `BaseProduct`, which defines generic relations to both inventory and reviews, allowing any product (Earwear, Neckwear, Fingerwear, Wristwear) to be linked to multiple inventory records and reviews without duplicating code.
    -   In `inventory.py`, the `Inventory` model uses `GenericForeignKey` to associate stock and pricing with any product type, supporting size variations and centralized inventory management.
    -   In `product.py`, each product category inherits this structure, making it easy to add new product types or attributes.

**Design rationale:**
Dedicated models for each product category (Earwear, Neckwear, etc.) allow the backend to efficiently query and manage each category without filtering a single large product table. This improves performance, keeps the codebase organized, and makes it easy to add category-specific features in the future. `GenericForeignKey` and `GenericRelation` are used to maintain flexible, DRY relationships for inventory and reviews across all categories.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## 3. Additional Requirements

### Object-Oriented Design

-   **Data encapsulation:** Business logic and data validation are encapsulated within dedicated service classes and model managers.

-   **Exception handling:** Error handling is implemented using try-except blocks and DRF exception classes, particularly for authentication and business-critical operations.

-   **Inheritance, abstraction, and polymorphism:** Product models leverage inheritance and abstract base classes, while polymorphic relationships are managed using Django's GenericForeignKey.

-   **Cohesion and loose coupling:** Each Django app (accounts, products, orders, shopping_bags, wishlists, common) encapsulates a distinct business domain, promoting strong cohesion and loose coupling across the backend.

-   **Code quality and readability:** All code adheres to PEP 8 (Python) and uses ESLint/Prettier (JavaScript) for consistent formatting and clear naming conventions.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### User Interface

-   **Custom design system:** All components use a consistent SCSS-based design system, ensuring visual harmony.

-   **Responsive design:** The UI is fully responsive, adapting to different screen sizes and devices.

-   **Component-based architecture:** The frontend is built with reusable, modular React components.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### User Experience

-   **Real-time feedback:** Forms provide instant validation feedback, with clear visual cues for valid, invalid, and focused states.

-   **Accessible and intuitive navigation:** The application uses clear navigation patterns and accessible controls.

-   **Consistent user experience:** All interactive elements, from buttons to forms and popups, follow a unified style and behavior.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

---

### Source Control System

**GitHub source control system is used for version control**

-   GitHub repository
-   Complete project history with 450+ commits over 4 months

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

---

## 🚀 Quick Start

### Installation

#### 1. Clone and setup

```bash
git clone https://github.com/BeatrisIlieva/drf-react-gems.git
cd drf-react-gems
```

---

#### 2. Backend environment variables

-   Copy `.env.example` to `.env` in the `server/` directory:
    ```bash
    cp server/.env.example server/.env
    ```
-   Edit `server/.env` and set your own secret key, database credentials, and Cloudinary credentials.

**Example `server/.env.example`:**

```env
# Django settings
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1],testserver

# Database settings
DB_NAME=django_react_gems_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

# Cloudinary settings
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

#### 3. Backend setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create PostgreSQL database
createdb drf_react_gems_db

# Run migrations
python manage.py migrate

# Populate database with products, reviews, and roles
python manage.py setup_database

# Start the backend server
python manage.py runserver
```

---

#### 4. Frontend environment variables

-   Copy `.env.example` to `.env.development` in the `client/` directory:
    ```bash
    cp client/.env.example client/.env.development
    ```
-   Edit `client/.env.development` and set your backend server URL.

**Example `client/.env.example`:**

```env
VITE_APP_SERVER_URL=http://localhost:8000  # (will be replaced with your deployed server URL)
```

---

#### 5. Frontend setup

```bash
cd ../client
npm install
npm start
```

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

### Database Population

The `python manage.py setup_database` command (run during installation) will:

-   Create all jewelry products with categories, collections, colors, metals, and stones
-   Add customer reviews with ratings and comments
-   Create admin users with different roles and permissions
-   Create a superuser with full system access

**Created Admin Users:**

-   Super User: `super_user@mail.com` | `!1Aabb`
-   Inventory User: `inventory_user@mail.com` | `!1Aabb`
-   Reviewer User: `reviewer_user@mail.com` | `!1Aabb`

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

## 📝 License

This project is licensed under the MIT License.

<p align="right" dir="auto"><a href="#drf-react-gems">Back To Top</a></p>

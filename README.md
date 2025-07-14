# 🛍️ DRF React Gems - E-commerce Platform

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.14+-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT%20Authentication-green.svg)](https://jwt.io/)
[![Azure](https://img.shields.io/badge/Azure%20Deployment-blue.svg)](https://azure.microsoft.com/)

A modern, full-stack e-commerce platform built with Django REST Framework (DRF) backend and React frontend. Features comprehensive user authentication, product management, shopping cart functionality, wishlist system, and secure payment processing.

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
-   [Unauthenticated User Permissions](#unauthenticated-user-permissions)
-   [Authenticated User Permissions](#authenticated-user-permissions)
-   [Admin Groups](#admin-groups)
-   [Exception Handling and Data Validation](#exception-handling-and-data-validation)

### 2. Bonus Features (15% Bonus)

-   [Testing Implementation](#testing-implementation)
-   [Asynchronous Views](#asynchronous-views)
-   [REST API Implementation](#rest-api-implementation)
-   [User Extension](#user-extension)
-   [Deployment](#deployment)
-   [Additional Functionality](#additional-functionality)

### 3. Additional Requirements

-   [Object-Oriented Design](#object-oriented-design)
-   [User Interface](#user-interface)
-   [User Experience](#user-experience)
-   [Source Control System](#source-control-system)

---

## 1. General Requirements

### Django Framework Implementation ✅

**The application is implemented using Django Framework:**

-   Complete Django configuration with DRF, JWT, CORS, and database settings (`server/src/settings.py`)

**The application has 11 page components:**

-   Home page (`client/src/components/pages/home/Home.jsx`)
-   Product list page (`client/src/components/pages/product-list/ProductList.jsx`)
-   Product item page (`client/src/components/pages/product-item/ProductItem.jsx`)
-   Shopping bag page (`client/src/components/pages/shopping-bag/ShoppingBag.jsx`)
-   Wishlist page (`client/src/components/pages/wishlist/Wishlist.jsx`)
-   Checkout page (`client/src/components/pages/checkout/Checkout.jsx`)
-   Payment page (`client/src/components/pages/payment/Payment.jsx`)
-   Order confirmation page (`client/src/components/pages/order-confirmation/OrderConfirmation.jsx`)
-   Login page (`client/src/components/pages/login/Login.jsx`)
-   Register page (`client/src/components/pages/register/Register.jsx`)
-   Accounts page (`client/src/components/pages/accounts/Accounts.jsx`)

**The application has 15 independent class-based views:**

-   BaseProductListView (`server/src/products/views/base.py`)
-   BaseProductItemView (`server/src/products/views/base.py`)
-   BaseAttributeView (`server/src/products/views/base.py`)
-   AsyncBaseAttributeView (`server/src/products/views/base.py`)
-   OrderViewSet (`server/src/orders/views.py`)
-   ShoppingBagViewSet (`server/src/shopping_bags/views.py`)
-   WishlistViewSet (`server/src/wishlists/views.py`)
-   ReviewViewSet (`server/src/products/views/review.py`)
-   UserRegisterView (`server/src/accounts/views/user_credential.py`)
-   UserLoginView (`server/src/accounts/views/user_credential.py`)
-   UserLogoutView (`server/src/accounts/views/user_credential.py`)
-   PasswordChangeView (`server/src/accounts/views/user_credential.py`)
-   UserDeleteView (`server/src/accounts/views/user_credential.py`)
-   UserProfileView (`server/src/accounts/views/user_profile.py`)
-   PhotoUploadView (`server/src/accounts/views/user_photo.py`)

**The application has 12 independent models:**

-   UserCredential (`server/src/accounts/models/user_credential.py`)
-   Order (`server/src/orders/models.py`)
-   BaseProduct (`server/src/products/models/base.py`)
-   Collection (`server/src/products/models/product.py`)
-   Color (`server/src/products/models/product.py`)
-   Metal (`server/src/products/models/product.py`)
-   Stone (`server/src/products/models/product.py`)
-   Inventory (`server/src/products/models/inventory.py`)
-   Size (`server/src/products/models/base.py`)
-   Review (`server/src/products/models/review.py`)
-   ShoppingBag (`server/src/shopping_bags/models.py`)
-   Wishlist (`server/src/wishlists/models.py`)

**The application has 6 forms:**

-   User registration form (`server/src/accounts/serializers/user_credential.py`)
-   User login form (`server/src/accounts/serializers/user_credential.py`)
-   Password change form (`client/src/components/pages/accounts/details/Details.jsx`)
-   Product review form (`server/src/products/serializers/base.py`)
-   Delivery information form (`client/src/components/pages/checkout/Checkout.jsx`)
-   Payment form (`client/src/components/pages/payment/Payment.jsx`)

### Database Service ✅

**PostgreSQL database is used as the primary database:**

-   Database configuration with PostgreSQL 13+ (`server/src/settings.py`)

**Multiple storage systems are utilized:**

-   Cloudinary: User profile photos stored in Cloudinary (`server/src/accounts/models/user_photo.py`)

### Frontend Implementation ✅

**React components are used for the frontend:**

-   React-based Single Page Application (SPA) (`client/src/App.jsx`)

### Web Page Design ✅

**Custom SCSS-based design system is implemented:**

-   SCSS modules for component-based styling (`client/src/styles/`)

### Authentication Functionality ✅

**The application has login/register/logout/delete account functionality:**

-   Complete JWT-based authentication system
-   Registration: UserRegistrationView (`server/src/accounts/views/user_credential.py`)
-   Login: UserLoginView (`server/src/accounts/views/user_credential.py`)
-   Logout: UserLogoutView (`server/src/accounts/views/user_credential.py`)
-   Account deletion: UserDeleteView (`server/src/accounts/views/user_credential.py`)

### Public Part ✅

**Public part is accessible by everyone:**

-   Anonymous users can browse products and use guest shopping cart/wishlist
-   Items are transferred to user account after login/register

**Note:**
Guest users can add items to their shopping bag and wishlist. Each guest’s data is securely isolated using a unique guest ID, ensuring that no guest can access or modify another user’s data. All inventory validation is performed on the backend, so users—whether guests or authenticated—cannot add more items than are available in stock. If a guest registers or logs in, their shopping bag and wishlist are safely migrated to their new account, with checks for duplicates and out-of-stock items. This approach is industry standard for modern e-commerce, provides a smooth user experience, and fully meets the project’s requirements for public/private data access and security.

### Private Part ✅

**Private part is accessible only by authenticated users and admins:**

-   Protected routes requiring authentication or admin status
-   Checkout, account management, review moderation
-   Users can create, read, update, delete their own data
-   Amazon-style checkout: Users can add items to cart as guests, but must authenticate to complete checkout (`client/src/components/pages/checkout/Checkout.jsx`)

**Review Moderation & Approval System:**

-   **Regular users** can only see reviews that have been approved for a product
-   **Reviewers** (users in the "reviewer" group with the `products.approve_review` permission) can see all reviews (approved and unapproved) for a product
-   **Reviewers** can approve or unapprove reviews directly from the product item page via dedicated controls
-   **Backend**: A dedicated DRF endpoint `/api/products/<category>/<pk>/all-reviews/` returns all reviews for a product, accessible only to reviewers
-   **Frontend**: The UI conditionally fetches and displays all reviews for reviewers, and only approved reviews for regular users. Approve/unapprove buttons are visible only to reviewers

### Customized Admin Site ✅

**Custom Django admin with Unfold framework and at least 5 custom options is implemented:**

-   Unfold Framework: Modern admin interface with custom themes, and styling (`server/src/unfold.py`)
-   Custom Navigation: Organized sidebar with collapsible sections for Users & Groups, Products, Product Attributes, and Reviews
-   Permission-Based Access: Different admin sections visible based on user permissions

### Admin Groups ✅

**3 admin groups with different permission levels are implemented:**

#### **Superuser (Full CRUD Access):**

-   Complete system administration with all CRUD operations
-   Full access to all admin sections including Users & Groups
-   Can manage users, groups, all products, orders, reviews, etc.
-   Access to all navigation sections in the admin interface

#### **Inventory Group (Product Management):**

-   Full CRUD access to products, inventory, and attributes
-   Can manage all product categories (Earwear, Fingerwear, Neckwear, Wristwear)
-   Access to Products and Product Attributes sections
-   User: `inventory_user@mail.com` | `@dmin123`

#### **Reviewer Group (Review Moderation):**

-   Can approve, and disapprove customer reviews for products they have purchased.
-   Access to Product Reviews section
-   User: `reviewer_user@mail.com` | `@dmin123`

**User roles are managed from the admin site:**

-   Django admin interface for role management

**Role management is secure and error-safe:**

-   Proper permission checks and error handling

**Automated Setup:**

-   All admin groups and their associated users are created automatically by a management command (`server/src/accounts/management/commands/create_roles.py`)

### Exception Handling and Data Validation ✅

**Comprehensive exception handling and data validation is implemented:**

-   **Server-side:**

    -   Password validation: All password changes and registrations are validated using custom logic to enforce strong password policies. (`server/src/accounts/validators/password.py`)
    -   Payment & order validation: All payment details (card number, expiry, CVV, cardholder name) are strictly validated using regex and business rules before processing orders. (`server/src/orders/services.py`)
    -   Model & serializer validation: All user input is validated at the serializer and model level, ensuring only valid data is saved to the database.
    -   Comprehensive exception handling: All API endpoints use DRF’s exception handling to return clear, actionable error messages for invalid input, authentication errors, and business logic violations.

-   **Client-side:**
    -   Real-time form validation: All forms (registration, login, delivery, payment, password update, etc.) provide instant feedback as users type, using custom React hooks and validation helpers. (`client/src/hooks/useForm.js`)
    -   Password update form: Displays backend errors if the user enters an incorrect current password or tries to reuse their old password, guiding the user to correct the issue. (`client/src/components/pages/accounts/details/password-update-form/PasswordUpdateForm.jsx`)
    -   Login form: Displays clear error messages if the user enters an incorrect email/username or password, reflecting backend authentication errors.
    -   Registration form: If a user tries to register with an email that is already in use, the backend error is shown in the form, helping the user resolve the conflict.
    -   Visual feedback with green/red/blue states: Input fields dynamically change color to indicate validation state (green for valid, red for invalid, blue for focus). (`client/src/styles/forms.scss`)
    -   Automatic focus on errors: When a form is submitted with errors, the first invalid input is automatically focused for user convenience. (`client/src/hooks/useFocusOnInvalidInput.js`)
    -   Server-side error integration: Any validation errors returned from the backend are mapped to the correct form fields and displayed to the user in real time. (`client/src/components/reusable/input-field/InputField.jsx`)

**Appropriate messages are shown to users during validation:**

-   Visual feedback with green/red/blue states
-   Real-time validation feedback
-   Clear, contextual error messages are shown next to the relevant input fields, with concise and user-friendly language.

## 2. Bonus Features

### Testing Implementation ✅

**The project includes around 200 automated tests, ensuring robust quality and reliability across all backend features.**

-   Shows 90%+ coverage (`coverage run manage.py test && coverage report`)
-   Runs all tests (`python manage.py test`)

### Asynchronous Views ✅

**High-performance asynchronous views are implemented to optimize user experience and server efficiency.**

-   Asynchronous endpoints allow the backend to handle multiple filter and product data requests concurrently, reducing wait times for users.
-   Database queries are optimized for speed and scalability, especially when the frontend needs to fetch several filters or product lists at once.
-   Implementation example: Async product listing and attribute filtering (`server/src/products/views/base.py`)

### REST API Implementation ✅

**The entire backend is built with Django REST Framework (DRF), exposing all business logic as RESTful API endpoints consumed by the React frontend.**

- No traditional Django HTML views—everything is handled via DRF API views and serializers.
- All features (authentication, products, shopping bag, wishlist, orders, reviews) are accessible through REST endpoints.

**Key files:**
- API views: (`server/src/accounts/views/`, `server/src/products/views/`, `server/src/orders/views.py`, `server/src/shopping_bags/views.py`, `server/src/wishlists/views.py`)
- Serializers: (`server/src/accounts/serializers/`, `server/src/products/serializers/`, `server/src/orders/serializers.py`, etc.)

### User Extension ✅

**The default Django user model is fully extended to support modern authentication and user management needs.**

- **Custom user model:**  
  Uses email as the primary login identifier, with unique username and additional fields for marketing consent.  
  (`server/src/accounts/models/user_credential.py`)

- **User profile:**  
  Stores personal and shipping information in a dedicated profile model linked one-to-one with the user.  
  (`server/src/accounts/models/user_profile.py`)

- **User photo:**  
  Handles user profile pictures with cloud storage and automatic optimization.  
  (`server/src/accounts/models/user_photo.py`)

- **Flexible authentication:**  
  Custom authentication backend allows login with either email or username, supporting case-insensitive authentication.  
  (`server/src/accounts/authentication.py`)

- **Automatic profile and photo creation:**  
  Django signals ensure that every new user automatically gets a profile and photo record.  
  (`server/src/accounts/signals.py`)

### Deployment ✅

**Azure App Service deployment is implemented**

-   Production deployment with CI/CD pipeline and environment configuration

### Additional Functionality ✅

- **Polymorphic product relationships:**
  The products app uses Django's `GenericForeignKey` and `GenericRelation` to enable flexible, polymorphic relationships between products, inventory, and reviews. 
  - In `base.py`, all product types inherit from `BaseProduct`, which defines generic relations to both inventory and reviews, allowing any product (Earwear, Neckwear, Fingerwear, Wristwear) to be linked to multiple inventory records and reviews without duplicating code.
  - In `inventory.py`, the `Inventory` model uses `GenericForeignKey` to associate stock and pricing with any product type, supporting size variations and centralized inventory management.
  - In `product.py`, each product category inherits this structure, making it easy to add new product types or attributes.

**Design rationale:**
Dedicated models for each product category (Earwear, Neckwear, etc.) allow the backend to efficiently query and manage each category without filtering a single large product table. This improves performance, keeps the codebase organized, and makes it easy to add category-specific features in the future. `GenericForeignKey` and `GenericRelation` are used to maintain flexible, DRY relationships for inventory and reviews across all categories.

**Benefits:**
- **Flexibility:** Easily support new product types and relationships without schema changes.
- **Scalability:** Centralized inventory and review logic for all products.
- **DRY code:** Avoids duplication by using abstract base classes and generic relations.
- **Extensibility:** New product categories or features can be added with minimal changes to the codebase.

**Key files:**
- Base product and generic relations (`server/src/products/models/base.py`)
- Inventory model with GenericForeignKey (`server/src/products/models/inventory.py`)
- Product category models (`server/src/products/models/product.py`)

## 3. Additional Requirements

### Object-Oriented Design ✅

**The project follows modern object-oriented design principles and best practices throughout the codebase:**

- **Data encapsulation:**
  User data and business logic are encapsulated within dedicated models and methods, ensuring maintainability and security.  
  (`server/src/accounts/models/user_credential.py`)

- **Exception handling:**
  Robust error handling is implemented using try-except blocks, particularly for authentication and business-critical operations.  
  (`server/src/accounts/views/user_credential.py`)

- **Inheritance, abstraction, and polymorphism:**
  Product models leverage inheritance and abstract base classes, while polymorphic relationships are managed using Django's GenericForeignKey for maximum flexibility.  
  (`server/src/products/models/base.py`)

- **Cohesion and loose coupling:**
  Each Django app (accounts, products, orders, shopping_bags, wishlists, common) encapsulates a distinct business domain, promoting strong cohesion and loose coupling across the backend.  
  (`server/src/`)

- **Code quality and readability:**
  All code adheres to PEP 8 (Python) and uses ESLint/Prettier (JavaScript) for consistent formatting and clear naming conventions.  
  (e.g., `createShoppingBagHandler`, `useProductItemContext`)

### User Interface & Experience ✅

**The project delivers a visually appealing and highly usable interface, with a strong focus on both design consistency and user experience.**

- **Custom design system:**  
  All components use a consistent SCSS-based design system, ensuring visual harmony and easy theming.  
  (`client/src/styles/_variables.scss`)

- **Responsive design:**  
  The UI is fully responsive, adapting seamlessly to different screen sizes and devices.

- **Component-based architecture:**  
  The frontend is built with reusable, modular React components, promoting maintainability and scalability.  
  (`client/src/components/`)

- **Real-time feedback:**  
  Forms provide instant validation feedback, with clear visual cues for valid, invalid, and focused states.  
  (`client/src/hooks/useForm.js`, `client/src/styles/forms.scss`)

- **Smooth user flows:**  
  Features like the mini bag popup, dynamic product filtering, and automatic focus on invalid inputs enhance usability and reduce friction.  
  (`client/src/components/pages/product-item/main-content/user-action/mini-bag-popup/MiniBagPopup.jsx`)

- **Accessible and intuitive navigation:**  
  The application uses clear navigation patterns, accessible controls, and user-friendly error messages.

- **Consistent user experience:**  
  All interactive elements, from buttons to forms, follow a unified style and behavior, ensuring a professional and predictable experience.

---

### Source Control System ✅

**GitHub source control system is used for version control**

-   GitHub repository with comprehensive version control
-   Complete project history with 450+ commits over 4 months
-   Extensive development history with commits on multiple different days
-   Branch Management: Feature branches, pull requests, and code reviews
-   Collaboration: Team development with proper Git workflow

---

## 🚀 Quick Start

### Installation

1. **Clone and setup**

    ```bash
    git clone https://github.com/yourusername/drf-react-gems.git
    cd drf-react-gems
    ```

2. **Backend setup**

    ```bash
    cd server
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Database setup**

    ```bash
    # Create PostgreSQL database
    createdb drf_react_gems_db

    # Run migrations
    python manage.py migrate

    # Populate database with products, reviews, and roles
    python manage.py setup_database
    ```

4. **Frontend setup**
    ```bash
    cd ../client
    npm install
    npm start
    ```

### Database Population

The project includes a comprehensive setup command that creates:

-   **Products**: All jewelry items with categories, collections, colors, metals, stones
-   **Reviews**: Customer reviews with ratings and comments
-   **Admin Users**: 4 different admin roles with specific permissions
-   **Superuser**: Full system access

**Command**: `python manage.py setup_database`

**Created Admin Users**:

-   Super User: `super_user@mail.com` | `@dmin123`
-   Inventory User: `inventory_user@mail.com` | `@dmin123`
-   Manager User: `manager_user@mail.com` | `@dmin123`
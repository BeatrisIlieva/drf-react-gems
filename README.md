# 🛍️ DRF React Gems - E-commerce Platform

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.14+-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT%20Authentication-green.svg)](https://jwt.io/)
[![Azure](https://img.shields.io/badge/Azure%20Deployment-blue.svg)](https://azure.microsoft.com/)

A full-stack e-commerce platform built with Django REST Framework (DRF) backend and React frontend. Features comprehensive user authentication, product management, shopping cart functionality, wishlist system, and secure payment processing.

<!-- Place screenshots here -->
<!-- Example:
## 📸 Screenshots

![Home Page](screenshots/home.png)
![Product List](screenshots/product-list.png)
-->

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

**Data Normalization:** The database is organized to keep information tidy and avoid repeating the same data in different places. It follows the main rules of database design:

-   **First Normal Form (1NF):** Each table has columns that hold just one piece of information (no lists or groups in a single cell). For example, the `products_color` table has a column for the color name, and each row is a single color.
-   **Second Normal Form (2NF):** All details in a table are linked only to that table's main ID. For example, in the `products_inventory` table, the amount in stock and the price are linked to a specific product and size, so there’s no confusion or extra copies.
-   **Third Normal Form (3NF):** There are no “hidden” connections between details. For example, product features like color, metal, and stone are always stored in their own tables and linked by ID, so if we change a color’s name, it updates everywhere at once.

**Entity Relationship Diagram:**

![ERD](https://res.cloudinary.com/dpgvbozrb/image/upload/v1752592187/ERD.pgerd_w6i0a3.png)

**Multiple storage systems are utilized:**

-   Cloudinary: User profile photos are stored in Cloudinary (`server/src/accounts/models/user_photo.py`)

### Frontend Implementation ✅

-   React-based Single Page Application (SPA)

### Web Page Design ✅

-   Custom SCSS modules for component-based styling

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

> ⚠️ **Note:**  
> Guest users can add items to their shopping bag and wishlist, with each guest’s data isolated using a unique guest ID. All modifications—adding, removing, or updating items—are performed via API requests to the backend, which centrally enforces inventory validation and business rules. The frontend uses quantity information from the backend to prevent users from adding more items than are available or removing more than they have in their bag. When a guest registers or logs in, their shopping bag and wishlist are migrated to their new account, with checks to prevent duplicate items.
>
> This approach ensures data integrity, a smooth user experience, and prevents errors related to unavailable inventory.

### Private Part ✅

**The private part of the application is accessible only to authenticated users and admins:**

-   Access to checkout, account management, and order history requires authentication.

**Review Moderation & Approval System:**

-   **Regular users** can only see reviews that have been approved on a product item page
-   **Reviewers** (users in the "reviewer" group with the `products.approve_review` permission) can see all reviews (approved and unapproved) for a product
-   **Backend**: A dedicated DRF endpoint `/api/products/<category>/<pk>/all-reviews/` returns all reviews for a product, accessible only to reviewers
-   **Frontend**: The UI conditionally fetches and displays all reviews for reviewers, and only approved reviews for regular users. Approve/unapprove buttons are visible only to reviewers

### Customized Admin Site ✅

**Custom Django admin with Unfold framework:**

-   Unfold Framework: Modern admin interface with custom themes, and styling (`server/src/unfold.py`)
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

See implementation: (`server/src/products/admin.py`)

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

## 2. Bonus Features 

### Testing Implementation ✅

**The project includes around 130 automated tests, ensuring robust quality and reliability across all backend features.**

-   Shows 85%+ coverage (`coverage run manage.py test && coverage report`)
-   Runs all tests (`python manage.py test`)

### Asynchronous Views ✅

**Asynchronous views are implemented to optimize user experience and server efficiency for product attribute filtering.**

-   Asynchronous endpoints allow the backend to handle multiple filter and product data requests concurrently, reducing wait times for users.
-   Implementation example: Async product listing and attribute filtering (`server/src/products/views/base.py`)

### REST API Implementation ✅

-   The backend utilizes DRF API views and serializers to provide all features to the React frontend, rather than using Django’s traditional HTML templates.
-   All business logic—including authentication, products, shopping bag, wishlist, orders, and reviews—is exposed through RESTful API endpoints.

### Django User Extension ✅

-   **Custom user model:**  
    Uses email as the primary login identifier, with unique username and additional fields for marketing consent.  
    (`server/src/accounts/models/user_credential.py`)

-   **User profile:**  
    Stores personal and shipping information in a dedicated profile model linked one-to-one with the user.  
    (`server/src/accounts/models/user_profile.py`)

-   **User photo:**  
    Handles user profile pictures with cloud storage and automatic optimization.  
    (`server/src/accounts/models/user_photo.py`)

-   **Automatic profile and photo creation:**  
    Django signals ensure that every new user automatically gets a profile and photo record.  
    (`server/src/accounts/signals.py`)

### Deployment ✅

-   Azure App Service deployment is implemented

### Additional Functionality ✅

-   **Polymorphic product relationships:**
    The products app uses Django's `GenericForeignKey` and `GenericRelation` to enable flexible, polymorphic relationships between products, inventory, and reviews.
    -   In `base.py`, all product types inherit from `BaseProduct`, which defines generic relations to both inventory and reviews, allowing any product (Earwear, Neckwear, Fingerwear, Wristwear) to be linked to multiple inventory records and reviews without duplicating code.
    -   In `inventory.py`, the `Inventory` model uses `GenericForeignKey` to associate stock and pricing with any product type, supporting size variations and centralized inventory management.
    -   In `product.py`, each product category inherits this structure, making it easy to add new product types or attributes.

**Design rationale:**
Dedicated models for each product category (Earwear, Neckwear, etc.) allow the backend to efficiently query and manage each category without filtering a single large product table. This improves performance, keeps the codebase organized, and makes it easy to add category-specific features in the future. `GenericForeignKey` and `GenericRelation` are used to maintain flexible, DRY relationships for inventory and reviews across all categories.

**Key files:**

-   Base product and generic relations (`server/src/products/models/base.py`)
-   Inventory model with GenericForeignKey (`server/src/products/models/inventory.py`)
-   Product category models (`server/src/products/models/product.py`)

## 3. Additional Requirements

### Object-Oriented Design ✅

- [Data Encapsulation](#data-encapsulation)
- [Exception Handling](#exception-handling)
- [Inheritance, Abstraction, and Polymorphism](#inheritance-abstraction-and-polymorphism)
- [Cohesion and Loose Coupling](#cohesion-and-loose-coupling)
- [Code Quality and Readability](#code-quality-and-readability)

### Data Encapsulation
Business logic and data validation are encapsulated within dedicated service classes and model managers, such as `ShoppingBagService` ([server/src/shopping_bags/services.py]) and `UserCredentialManager` ([server/src/accounts/managers/user_credential.py]). This ensures that critical operations—like inventory validation, atomic updates, and secure user creation—are only accessible through well-defined interfaces, promoting maintainability and security.

### Exception Handling
Robust error handling is implemented using try-except blocks and DRF exception classes, particularly for authentication and business-critical operations. For example, authentication and registration logic in `UserCredentialViewSet` ([server/src/accounts/views/user_credential.py]) uses structured exception handling to provide clear API error responses. Service classes such as `ShoppingBagService` ([server/src/shopping_bags/services.py]) and `OrderService` ([server/src/orders/services.py]) consistently raise and handle exceptions for validation errors, inventory issues, and transactional integrity. This approach ensures that all errors are managed in a predictable, secure, and user-friendly manner across the backend.

### Inheritance, Abstraction, and Polymorphism
Product models leverage inheritance and abstract base classes, while polymorphic relationships are managed using Django's GenericForeignKey for maximum flexibility.  
([server/src/products/models/base.py])

### Cohesion and Loose Coupling
Each Django app (accounts, products, orders, shopping_bags, wishlists, common) encapsulates a distinct business domain, promoting strong cohesion and loose coupling across the backend.  
([server/src/])

### Code Quality and Readability
All code adheres to PEP 8 (Python) and uses ESLint/Prettier (JavaScript) for consistent formatting and clear naming conventions.  
(e.g., `createShoppingBagHandler`, `useProductItemContext`)

### User Interface & Experience ✅

**The project delivers a visually appealing and highly usable interface, with a strong focus on both design consistency and user experience.**

-   **Custom design system:**  
    All components use a consistent SCSS-based design system, ensuring visual harmony and easy theming.  
    (`client/src/styles/_variables.scss`)

-   **Responsive design:**  
    The UI is fully responsive, adapting seamlessly to different screen sizes and devices.

-   **Component-based architecture:**  
    The frontend is built with reusable, modular React components, promoting maintainability and scalability.  
    (`client/src/components/`)

-   **Real-time feedback:**  
    Forms provide instant validation feedback, with clear visual cues for valid, invalid, and focused states.  
    (`client/src/hooks/useForm.js`, `client/src/styles/forms.scss`)

-   **Smooth user flows:**  
    Features like the mini bag popup, dynamic product filtering, and automatic focus on invalid inputs enhance usability and reduce friction.  
    (`client/src/components/pages/product-item/main-content/user-action/mini-bag-popup/MiniBagPopup.jsx`)

-   **Accessible and intuitive navigation:**  
    The application uses clear navigation patterns, accessible controls, and user-friendly error messages.

-   **Consistent user experience:**  
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
    git clone https://github.com/BeatrisIlieva/drf-react-gems.git
    cd drf-react-gems
    ```

2. **Backend setup**

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

    python manage.py runserver
    ```

3. **Frontend setup**
    ```bash
    cd ../client
    npm install
    npm start
    ```

### Database Population

The project includes a setup command that creates:

-   **Products**: All jewelry items with categories, collections, colors, metals, stones
-   **Reviews**: Customer reviews with ratings and comments
-   **Admin Users**: 2 different admin roles with specific permissions
-   **Superuser**: Full system access

**Command**: `python manage.py setup_database`

**Created Admin Users**:

-   Super User: `super_user@mail.com` | `!1Aabb`
-   Inventory User: `inventory_user@mail.com` | `!1Aabb`
-   Reviewer User: `reviewer_user@mail.com` | `!1Aabb`

## 📝 License

This project is licensed under the MIT License.

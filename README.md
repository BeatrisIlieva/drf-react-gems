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
- [Django Framework Implementation](#django-framework-implementation)
- [Database Service](#database-service)
- [Frontend Implementation](#frontend-implementation)
- [Web Page Design](#web-page-design)
- [Authentication Functionality](#authentication-functionality)
- [Public Part](#public-part)
- [Private Part](#private-part)
- [Customized Admin Site](#customized-admin-site)
- [Unauthenticated User Permissions](#unauthenticated-user-permissions)
- [Authenticated User Permissions](#authenticated-user-permissions)
- [Admin Groups](#admin-groups)
- [Exception Handling and Data Validation](#exception-handling-and-data-validation)

### 2. Bonus Features (15% Bonus)
- [Testing Implementation](#testing-implementation)
- [Asynchronous Views](#asynchronous-views)
- [REST API Implementation](#rest-api-implementation)
- [User Extension](#user-extension)
- [Deployment](#deployment)
- [Additional Functionality](#additional-functionality)

### 3. Additional Requirements
- [Object-Oriented Design](#object-oriented-design)
- [User Interface](#user-interface)
- [User Experience](#user-experience)
- [Source Control System](#source-control-system)

---

## 1. General Requirements

### Django Framework Implementation ✅

**The application is implemented using Django Framework:**
- Complete Django configuration with DRF, JWT, CORS, and database settings (`server/src/settings.py`)

**The application has 11 page components:**
- Home page (`client/src/components/pages/home/Home.jsx`)
- Product list page (`client/src/components/pages/product-list/ProductList.jsx`)
- Product item page (`client/src/components/pages/product-item/ProductItem.jsx`)
- Shopping bag page (`client/src/components/pages/shopping-bag/ShoppingBag.jsx`)
- Wishlist page (`client/src/components/pages/wishlist/Wishlist.jsx`)
- Checkout page (`client/src/components/pages/checkout/Checkout.jsx`)
- Payment page (`client/src/components/pages/payment/Payment.jsx`)
- Order confirmation page (`client/src/components/pages/order-confirmation/OrderConfirmation.jsx`)
- Login page (`client/src/components/pages/login/Login.jsx`)
- Register page (`client/src/components/pages/register/Register.jsx`)
- Accounts page (`client/src/components/pages/accounts/Accounts.jsx`)

**The application has 15 independent class-based views:**
- BaseProductListView (`server/src/products/views/base.py`)
- BaseProductItemView (`server/src/products/views/base.py`)
- BaseAttributeView (`server/src/products/views/base.py`)
- AsyncBaseAttributeView (`server/src/products/views/base.py`)
- OrderViewSet (`server/src/orders/views.py`)
- ShoppingBagViewSet (`server/src/shopping_bags/views.py`)
- WishlistViewSet (`server/src/wishlists/views.py`)
- ReviewViewSet (`server/src/products/views/review.py`)
- UserRegisterView (`server/src/accounts/views/user_credential.py`)
- UserLoginView (`server/src/accounts/views/user_credential.py`)
- UserLogoutView (`server/src/accounts/views/user_credential.py`)
- PasswordChangeView (`server/src/accounts/views/user_credential.py`)
- UserDeleteView (`server/src/accounts/views/user_credential.py`)
- UserProfileView (`server/src/accounts/views/user_profile.py`)
- PhotoUploadView (`server/src/accounts/views/user_photo.py`)

**The application has 12 independent models:**
- UserCredential (`server/src/accounts/models/user_credential.py`)
- Order (`server/src/orders/models.py`)
- BaseProduct (`server/src/products/models/base.py`)
- Collection (`server/src/products/models/product.py`)
- Color (`server/src/products/models/product.py`)
- Metal (`server/src/products/models/product.py`)
- Stone (`server/src/products/models/product.py`)
- Inventory (`server/src/products/models/inventory.py`)
- Size (`server/src/products/models/base.py`)
- Review (`server/src/products/models/review.py`)
- ShoppingBag (`server/src/shopping_bags/models.py`)
- Wishlist (`server/src/wishlists/models.py`)

**The application has 6 forms:**
- User registration form (`server/src/accounts/serializers/user_credential.py`)
- User login form (`server/src/accounts/serializers/user_credential.py`)
- Password change form (`client/src/components/pages/accounts/details/Details.jsx`)
- Product review form (`server/src/products/serializers/base.py`)
- Delivery information form (`client/src/components/pages/checkout/Checkout.jsx`)
- Payment form (`client/src/components/pages/payment/Payment.jsx`)

### Database Service ✅

**PostgreSQL database is used as the primary database:**
- Database configuration with PostgreSQL 13+ (`server/src/settings.py`)

**Multiple storage systems are utilized:**
- Cloudinary: User profile photos stored in Cloudinary (`server/src/accounts/models/user_photo.py`)

### Frontend Implementation ✅

**React components are used for the frontend:**
- React-based Single Page Application (SPA) (`client/src/App.jsx`)

### Web Page Design ✅

**Custom SCSS-based design system is implemented:**
- SCSS modules for component-based styling (`client/src/styles/`)

### Authentication Functionality ✅

**The application has login/register/logout/delete account functionality:**
- Complete JWT-based authentication system
- Registration: UserRegistrationView (`server/src/accounts/views/user_credential.py`)
- Login: UserLoginView (`server/src/accounts/views/user_credential.py`)
- Logout: UserLogoutView (`server/src/accounts/views/user_credential.py`)
- Account deletion: UserDeleteView (`server/src/accounts/views/user_credential.py`)

### Public Part ✅

**Public part is accessible by everyone:**
- Anonymous users can browse products and use guest shopping cart/wishlist
- AuthGuard (`client/src/guards/AuthGuard.jsx`)
- Product browsing, product details
- Items are transferred to user account after login/register

### Private Part ✅

**Private part is accessible only by authenticated users and admins:**
- Protected routes requiring authentication or admin status
- Custom permission class: IsReviewer (`src/common/permissions.py`)
- AuthGuard (`client/src/guards/AuthGuard.jsx`)
- Checkout, account management, review moderation

**Review Moderation & Approval System:**
- **Regular users** can only see reviews that have been approved for a product
- **Reviewers** (users in the "reviewer" group with the `products.approve_review` permission) can see all reviews (approved and unapproved) for a product
- **Reviewers** can approve or unapprove reviews directly from the product item page via dedicated controls
- **Backend**: A dedicated DRF endpoint `/api/products/<category>/<pk>/all-reviews/` returns all reviews for a product, accessible only to reviewers
- **Frontend**: The UI conditionally fetches and displays all reviews for reviewers, and only approved reviews for regular users. Approve/unapprove buttons are visible only to reviewers

### Customized Admin Site ✅

**Custom Django admin with Unfold framework and 5 custom options is implemented:**
- Custom Django admin with Unfold framework and 5 custom options
- Unfold (`server/src/unfold.py`)
- Unfold Framework: Modern admin interface with custom navigation, themes, and styling
- Custom Navigation: Organized sidebar with collapsible sections for Users & Groups, Products, Product Attributes, and Reviews
- Permission-Based Access: Different admin sections visible based on user permissions
- Product Management: Product filtering by category and availability (`server/src/products/admin.py`)
- Order Management: Order status management (`server/src/orders/admin.py`)
- User Management: User role management (`server/src/accounts/admin.py`)
- Review Moderation: Review moderation tools (`server/src/products/admin.py`)
- Inventory Tracking: Inventory tracking (`server/src/products/admin.py`)

### Unauthenticated User Permissions ✅

**Unauthenticated users have only 'get' permissions:**
- Anonymous users can only browse and view products
- ProductListView allows GET requests from all users (`server/src/products/views/base.py`)
- GET requests for product browsing, POST for login/register

### Authenticated User Permissions ✅

**Authenticated users have full CRUD access to their content:**
- Users can create, read, update, delete their own data
- Users can manage their own shopping cart (`server/src/shopping_bags/views.py`)
- Amazon-style checkout: Users can add items to cart as guests, but must authenticate to complete checkout (`client/src/components/pages/checkout/Checkout.jsx`)

### Admin Groups ✅

**4 admin groups with different permission levels are implemented:**
- Creates all admin groups and users (`server/src/accounts/management/commands/create_roles.py`)
- Custom admin interface with role-based navigation (`server/src/unfold.py`)

#### **Superuser (Full CRUD Access):**
- Complete system administration with all CRUD operations
- Full access to all admin sections including Users & Groups
- Can manage users, groups, all products, orders, reviews, and system configuration
- Access to all navigation sections in the admin interface

#### **Inventory Group (Product Management):**
- Full CRUD access to products, inventory, and attributes
- Can manage all product categories (Earwear, Fingerwear, Neckwear, Wristwear)
- Can add, edit, delete products, manage inventory, and update product attributes
- Access to Products and Product Attributes sections
- User: `inventory_user@mail.com` | `@dmin123`

#### **Manager Group (View-Only Access):**
- View-only access to all products and orders
- Can view but cannot modify products, orders, or user data
- Read-only access for monitoring and reporting purposes
- Limited access to view-only sections
- User: `manager_user@mail.com` | `@dmin123`

#### **Reviewer Group (Review Moderation):**
- Review approval and moderation permissions
- Can approve, reject, and manage product reviews
- Review moderation tools, can change review status and manage comments
- Access to Product Reviews section
- User: `reviewer_user@mail.com` | `@dmin123`

**User roles are managed from the admin site:**
- Django admin interface for role management
- User role management in admin (`server/src/accounts/admin.py`)

**Role management is secure and error-safe:**
- Proper permission checks and error handling
- Secure authentication with proper error handling (`server/src/accounts/views/user_credential.py`)

### Exception Handling and Data Validation ✅

**Comprehensive exception handling and data validation is implemented:**
- Server-side: Password validation (`server/src/accounts/validators/password.py`)
- Client-side: Real-time password validation (`client/src/components/reusable/password-validator/PasswordValidator.jsx`)
- Form validation: Registration form with validation (`client/src/components/pages/register/Register.jsx`)

**Appropriate messages are shown to users during validation:**
- Visual feedback with green/red/blue states
- Real-time validation feedback (`client/src/components/reusable/input-field/InputField.jsx`)

## 2. Bonus Features (15% Bonus)

### Testing Implementation ✅

**90%+ test coverage with comprehensive backend tests**
- Runs all tests (`python manage.py test`)
- Shows 90%+ coverage (`coverage run manage.py test && coverage report`)
- All Test Files:
  - Backend tests: Product view tests (`server/tests/products/views/test_product.py`)
  - API tests: Authentication tests (`server/tests/accounts/views/test_user_credential.py`)

### Asynchronous Views ✅

**Asynchronous views are implemented for better performance**
- Async product listing with database optimization (`server/src/products/views/base.py`)

### REST API Implementation ✅

**Complete REST API with Django REST Framework is implemented**
- All API Components:
  - Product serializers (`server/src/products/serializers/base.py`)
  - User serializers (`server/src/accounts/serializers/user_credential.py`)
  - Order serializers (`server/src/orders/serializers.py`)

### User Extension ✅

**Django user is extended with additional fields**
- Extended user with email, username, and profile fields (`server/src/accounts/models/user_credential.py`)

### Deployment ✅

**Azure App Service deployment is implemented**
- Production deployment with CI/CD pipeline and environment configuration

### Additional Functionality ✅

**Multiple additional features with practical use are implemented**
- Wishlist: Complete wishlist functionality (`server/src/wishlists/models.py`)
- Real-time validation: PasswordValidator (`client/src/components/reusable/password-validator/PasswordValidator.jsx`)
- Mini bag popup: MiniBagPopup (`client/src/components/pages/product-item/main-content/user-action/mini-bag-popup/MiniBagPopup.jsx`)
- GenericForeignKey: Review model uses GenericForeignKey for polymorphic relationships (`server/src/products/models/review.py`)

## 3. Additional Requirements

### Object-Oriented Design ✅

**Data encapsulation is properly implemented**
- Encapsulated user data with proper methods (`server/src/accounts/models/user_credential.py`)

**Exception handling is properly implemented**
- Try-catch blocks for authentication errors (`server/src/accounts/views/user_credential.py`)

**Inheritance, abstraction, and polymorphism are properly implemented**
- Product model inheritance and polymorphic relationships with GenericForeignKey (`server/src/products/models/base.py`)

**Strong cohesion and loose coupling principles are followed**
- Separate contexts for different concerns (User, ShoppingBag, Wishlist) (`client/src/contexts/`)

**Code is correctly formatted and structured**
- All Code Quality Features:
  - Python: PEP 8 compliance with proper indentation
  - JavaScript: ESLint and Prettier for consistent formatting
  - Clear naming: `createShoppingBagHandler`, `useProductItemContext`

### User Interface ✅

**Visually appealing user interface is implemented**
- Custom design system with consistent styling (`client/src/styles/_variables.scss`)

### User Experience ✅

**Good user experience is implemented**
- All UX Features:
  - Responsive design: Desktop-first approach with responsive breakpoints
  - Loading states: Smooth transitions and loading indicators
  - Error handling: User-friendly error messages and recovery
  - Navigation: Intuitive routing with breadcrumbs and navigation guards

### Source Control System ✅

**GitHub source control system is used for version control**
- GitHub repository with comprehensive version control
- Complete project history with 450+ commits over 4 months
- Extensive development history with commits on multiple different days
- Branch Management: Feature branches, pull requests, and code reviews
- Collaboration: Team development with proper Git workflow

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
- **Products**: All jewelry items with categories, collections, colors, metals, stones
- **Reviews**: Customer reviews with ratings and comments
- **Admin Users**: 4 different admin roles with specific permissions
- **Superuser**: Full system access

**Command**: `python manage.py setup_database`

**Created Admin Users**:
- Super User: `super_user@mail.com` | `@dmin123`
- Inventory User: `inventory_user@mail.com` | `@dmin123`
- Manager User: `manager_user@mail.com` | `@dmin123`
- Reviewer User: `reviewer_user@mail.com` | `@dmin123`

---

**Built with ❤️ using Django, React, and modern web technologies**
# Wishlist API Documentation

## Overview
The wishlist functionality allows both authenticated users and guest users to save products they are interested in. Guest users are identified by a `guest_id` UUID, while authenticated users are identified by their user account.

## API Endpoints

### 1. List Wishlist Items
**GET** `/wishlist/`

Lists all wishlist items for the current user (authenticated or guest).

**Parameters:**
- `guest_id` (query parameter): Required for guest users to identify their wishlist

**Authentication:** Not required (supports both authenticated and guest users)

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "user": null,
      "guest_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2025-06-26T10:30:00Z",
      "content_type": "earwear",
      "object_id": 1,
      "product_info": {
        "id": 1,
        "first_image": "http://example.com/image1.jpg",
        "second_image": "http://example.com/image2.jpg",
        "collection": "Vintage Collection",
        "color": "Gold",
        "metal": "Gold",
        "stone": "Diamond",
        "product_type": "earwear"
      }
    }
  ]
}
```

### 2. Add Product to Wishlist
**POST** `/wishlist/add/`

Adds a product to the user's wishlist.

**Authentication:** Not required (supports both authenticated and guest users)

**Request Body:**
```json
{
  "content_type": "earwear",
  "object_id": 1,
  "guest_id": "123e4567-e89b-12d3-a456-426614174000"  // Required for guest users
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": null,
  "guest_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2025-06-26T10:30:00Z",
  "content_type": "earwear",
  "object_id": 1,
  "product_info": {
    "id": 1,
    "first_image": "http://example.com/image1.jpg",
    "second_image": "http://example.com/image2.jpg",
    "collection": "Vintage Collection",
    "color": "Gold",
    "metal": "Gold",
    "stone": "Diamond",
    "product_type": "earwear"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Item already in wishlist"
}
```

### 3. Remove Product from Wishlist
**DELETE** `/wishlist/remove/<content_type>/<object_id>/`

Removes a specific product from the user's wishlist.

**Parameters:**
- `content_type` (URL parameter): The type of product (earwear, neckwear, fingerwear, wristwear)
- `object_id` (URL parameter): The ID of the product
- `guest_id` (query parameter): Required for guest users

**Authentication:** Not required (supports both authenticated and guest users)

**Response (204 No Content):** Empty response body

**Error Response (404 Not Found):**
```json
{
  "detail": "Item not found in wishlist"
}
```

## Product Types
The following product types are supported:
- `earwear` - Earrings and ear accessories
- `neckwear` - Necklaces and neck accessories  
- `fingerwear` - Rings and finger accessories
- `wristwear` - Bracelets and wrist accessories

## Guest User Flow
1. Generate a UUID for the guest user on the frontend
2. Use this UUID as `guest_id` in all wishlist operations
3. When the user registers or logs in, pass the `guest_id` in the request headers
4. The system will automatically migrate guest wishlist items to the authenticated user

## Authentication Flow Integration
When a guest user registers or logs in, their wishlist items are automatically migrated to their authenticated account. This is handled by the `migrate_guest_data_to_user` function in the authentication process.

## Error Handling
- **400 Bad Request**: Invalid data, duplicate items, or missing required fields
- **401 Unauthorized**: Authentication required for certain operations
- **404 Not Found**: Product or wishlist item not found
- **500 Internal Server Error**: Server-side errors

## Database Constraints
- Each user (authenticated or guest) can only have one instance of each product in their wishlist
- The system prevents duplicate entries using unique constraints on (`user`, `content_type`, `object_id`) and (`guest_id`, `content_type`, `object_id`)

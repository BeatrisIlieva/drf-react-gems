from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import uuid

from src.products.models import Collection, Color, Metal, Stone, Size, Earwear, Inventory

UserModel = get_user_model()


class TestDataBuilder:
    """
    A utility class for creating shared test data across test classes.

    This class provides methods to create common test objects (users, products,
    collections, etc.) that can be reused across multiple test classes. 
    """

    @classmethod
    def create_shared_data(cls):
        # Create test user with unique email and username
        user = UserModel.objects.create_user(
            email='shared_test@example.com',
            username='shared_test_user',
            password='SharedTestPass123!'
        )

        # Create product-related objects
        collection = Collection.objects.create(name='Shared Test Collection')
        color = Color.objects.create(name='Shared Gold')
        metal = Metal.objects.create(name='Shared Gold')
        stone = Stone.objects.create(name='Shared Diamond')
        size = Size.objects.create(name='Shared Medium')

        # Create test earwear product
        earwear = Earwear.objects.create(
            first_image='https://shared.example.com/image1.jpg',
            second_image='https://shared.example.com/image2.jpg',
            collection=collection,
            color=color,
            metal=metal,
            stone=stone
        )

        # Create inventory for the earwear
        inventory = Inventory.objects.create(
            quantity=10,
            price=100.00,
            size=size,
            content_type=ContentType.objects.get_for_model(Earwear),
            object_id=earwear.id
        )

        # Get content types
        earwear_content_type = ContentType.objects.get_for_model(Earwear)
        inventory_content_type = ContentType.objects.get_for_model(Inventory)

        return {
            'user': user,
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
            'earwear': earwear,
            'inventory': inventory,
            'earwear_content_type': earwear_content_type,
            'inventory_content_type': inventory_content_type,
        }

    @classmethod
    def create_authenticated_user(cls, email_suffix='', username_suffix=''):
        unique_id = str(uuid.uuid4())[:8]
        email = f'auth_user{email_suffix}_{unique_id}@example.com'
        username = f'auth_user{username_suffix}_{unique_id}'

        return UserModel.objects.create_user(
            email=email,
            username=username,
            password='AuthUserPass123!'
        )

    @classmethod
    def create_product_with_inventory(cls, product_name='Test Product', price=100.00):
        unique_id = str(uuid.uuid4())[:4]
        # Create product-related objects
        collection = Collection.objects.create(
            name=f'{product_name[:10]} Col {unique_id}')
        color = Color.objects.create(
            name=f'{product_name[:10]} Color {unique_id}')
        metal = Metal.objects.create(
            name=f'{product_name[:10]} Metal {unique_id}')
        stone = Stone.objects.create(
            name=f'{product_name[:10]} Stone {unique_id}')
        size = Size.objects.create(
            name=f'{product_name[:10]} Size {unique_id}')

        # Create product
        product = Earwear.objects.create(
            first_image=f'https://{product_name.lower()}.example.com/image1.jpg',
            second_image=f'https://{product_name.lower()}.example.com/image2.jpg',
            collection=collection,
            color=color,
            metal=metal,
            stone=stone
        )

        # Create inventory
        inventory = Inventory.objects.create(
            quantity=10,
            price=price,
            size=size,
            content_type=ContentType.objects.get_for_model(Earwear),
            object_id=product.id
        )

        return {
            'product': product,
            'inventory': inventory,
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
            'content_type': ContentType.objects.get_for_model(Earwear),
        }

    @classmethod
    def create_unique_user(cls, email_prefix='test', username_prefix='testuser'):
        unique_id = str(uuid.uuid4())[:8]
        email = f'{email_prefix}_{unique_id}@example.com'
        username = f'{username_prefix}_{unique_id}'

        return UserModel.objects.create_user(
            email=email,
            username=username,
            password='TestPass123!'
        )

    @classmethod
    def create_unique_product_data(cls, prefix='Test'):
        unique_id = str(uuid.uuid4())[:4]

        collection = Collection.objects.create(
            name=f'{prefix[:10]} Col {unique_id}')
        color = Color.objects.create(name=f'{prefix[:10]} Color {unique_id}')
        metal = Metal.objects.create(name=f'{prefix[:10]} Metal {unique_id}')
        stone = Stone.objects.create(name=f'{prefix[:10]} Stone {unique_id}')
        size = Size.objects.create(name=f'{prefix[:10]} Size {unique_id}')

        return {
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
        }

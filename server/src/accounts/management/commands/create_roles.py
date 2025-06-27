from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from src.products.models import (
    Earwear,
    Neckwear,
    Fingerwear,
    Wristwear,
    Collection,
    Color,
    Metal,
    Stone,
    Size,
    Inventory
)
from src.products.models.review import Review


class Command(BaseCommand):
    help = 'Setup roles: superuser, Inventory group/user, Manager group/user'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        self.stdout.write(self.style.SUCCESS(
            'Starting creating roles and users...'
        ))

        # === Define model content types ===
        models_permissions = {
            Earwear: ['add', 'change', 'delete', 'view'],
            Neckwear: ['add', 'change', 'delete', 'view'],
            Fingerwear: ['add', 'change', 'delete', 'view'],
            Wristwear: ['add', 'change', 'delete', 'view'],
            Inventory: ['add', 'change', 'delete', 'view'],
            Size: ['add', 'change', 'delete', 'view'],
            Collection: ['add', 'change', 'delete', 'view'],
            Metal: ['add', 'change', 'delete', 'view'],
            Color: ['add', 'change', 'delete', 'view'],
            Stone: ['add', 'change', 'delete', 'view'],
            Review: ['approve_review'],
        }

        # === Create Inventory group with full CRUD ===
        inventory_group, _ = Group.objects.get_or_create(name='Inventory')

        for model, actions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                codename = f'{action}_{model._meta.model_name}'
                try:
                    perm = Permission.objects.get(
                        codename=codename, content_type=content_type)
                    inventory_group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Permission {codename} not found.'))

        # === Create Manager group with limited permissions ===
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        limited_actions = ['view']

        for model in models_permissions:
            content_type = ContentType.objects.get_for_model(model)
            for action in limited_actions:
                codename = f'{action}_{model._meta.model_name}'
                try:
                    perm = Permission.objects.get(
                        codename=codename, content_type=content_type)
                    manager_group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Permission {codename} not found.'))

        # === Create Reviewer group with review approval permissions ===
        reviewer_group, _ = Group.objects.get_or_create(name='Reviewer')

        # Add review-related permissions only
        review_content_type = ContentType.objects.get_for_model(Review)
        review_permissions = ['approve_review', 'view_review', 'change_review']

        for perm_codename in review_permissions:
            try:
                # For custom permissions like approve_review, use the exact codename
                if perm_codename == 'approve_review':
                    perm = Permission.objects.get(
                        codename=perm_codename, content_type=review_content_type)
                else:
                    # For standard permissions, use the model name
                    perm = Permission.objects.get(
                        codename=perm_codename, content_type=review_content_type)
                reviewer_group.permissions.add(perm)
                self.stdout.write(self.style.SUCCESS(
                    f'Added {perm_codename} permission to Reviewer group.'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Permission {perm_codename} not found.'))

        # === Create Inventory staff user ===
        inventory_user, created = User.objects.get_or_create(
            email='inventory_user@mail.com',
            username='inventory_user',
            defaults={'is_staff': True}
        )

        if created:
            inventory_user.set_password('@dmin123')
            inventory_user.save()
            self.stdout.write(self.style.SUCCESS('Inventory user created.'))
        inventory_user.groups.add(inventory_group)

        # === Create Manager staff user ===
        manager_user, created = User.objects.get_or_create(
            email='manager_user@mail.com',
            username='manager_user',
            defaults={'is_staff': True}
        )

        if created:
            manager_user.set_password('@dmin123')
            manager_user.save()
            self.stdout.write(self.style.SUCCESS('Manager user created.'))
        manager_user.groups.add(manager_group)

        # === Create Reviewer staff user ===
        reviewer_user, created = User.objects.get_or_create(
            email='reviewer_user@mail.com',
            username='reviewer_user',
            defaults={'is_staff': True}
        )

        if created:
            reviewer_user.set_password('@dmin123')
            reviewer_user.save()
            self.stdout.write(self.style.SUCCESS('Reviewer user created.'))
        reviewer_user.groups.add(reviewer_group)

        # === Create Superuser ===
        if not User.objects.filter(email='super_user@mail.com').exists():
            User.objects.create_superuser(
                email='super_user@mail.com', password='@dmin123')
            self.stdout.write(self.style.SUCCESS('Superuser created.'))

        self.stdout.write(self.style.SUCCESS(
            'All roles and users set up successfully.'))

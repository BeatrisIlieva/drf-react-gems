from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from src.products.models import ProductItem, ProductVariant, ProductItemStoneByColor


class Command(BaseCommand):
    help = 'Setup roles: superuser, Inventory group/user, Manager group/user'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # === Define model content types ===
        models_permissions = {
            ProductItem: ['add', 'change', 'delete', 'view'],
            ProductVariant: ['add', 'change', 'delete', 'view'],
            ProductItemStoneByColor: ['add', 'change', 'delete', 'view'],
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
        limited_actions = ['view', 'change']  # No add/delete

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

        # === Create Inventory staff user ===
        inventory_user, created = User.objects.get_or_create(
            email='inventory_user@mail.com',
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
            defaults={'is_staff': True}
        )
        if created:
            manager_user.set_password('@dmin123')
            manager_user.save()
            self.stdout.write(self.style.SUCCESS('Manager user created.'))
        manager_user.groups.add(manager_group)

        # === Create Superuser ===
        if not User.objects.filter(email='super_user@mail.com').exists():
            User.objects.create_superuser(
                email='super_user@mail.com', password='@dmin123')
            self.stdout.write(self.style.SUCCESS('Superuser created.'))

        self.stdout.write(self.style.SUCCESS(
            'All roles and users set up successfully.'))

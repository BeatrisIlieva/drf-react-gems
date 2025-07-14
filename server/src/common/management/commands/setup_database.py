from django.core.management.base import BaseCommand
from django.core.management import call_command

# python manage.py setup_database


class Command(BaseCommand):
    help = 'Setup database with products, reviews, and roles'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting database setup...')
        )

        try:
            self.stdout.write(
                self.style.SUCCESS('📦 Step 1/4: Creating products...')
            )
            call_command('create_products')
            self.stdout.write(
                self.style.SUCCESS('✅ Products created successfully!')
            )

            self.stdout.write(
                self.style.SUCCESS('⭐ Step 2/4: Creating reviews...')
            )
            call_command('create_reviews')
            self.stdout.write(
                self.style.SUCCESS('✅ Reviews created successfully!')
            )

            self.stdout.write(
                self.style.SUCCESS('👥 Step 3/4: Creating roles and users...')
            )
            call_command('create_roles')
            self.stdout.write(
                self.style.SUCCESS('✅ Roles and users created successfully!')
            )

            self.stdout.write(
                self.style.SUCCESS('🏠 Step 4/4: Creating addresses...')
            )

            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 Database setup completed successfully!'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    '🔑 Admin credentials:'
                )
            )
            self.stdout.write(
                '   • Super User: super_user@mail.com | !1Aabb')
            self.stdout.write(
                '   • Inventory User: inventory_user@mail.com | !1Aabb')
            self.stdout.write(
                '   • Reviewer User: reviewer_user@mail.com | !1Aabb')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during setup: {str(e)}')
            )
            raise e

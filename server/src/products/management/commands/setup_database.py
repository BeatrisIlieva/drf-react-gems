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
            # Step 1: Create products
            self.stdout.write(
                self.style.SUCCESS('📦 Step 1/3: Creating products...')
            )
            call_command('create_products')
            self.stdout.write(
                self.style.SUCCESS('✅ Products created successfully!')
            )

            # Step 2: Create reviews
            self.stdout.write(
                self.style.SUCCESS('⭐ Step 2/3: Creating reviews...')
            )
            call_command('create_reviews')
            self.stdout.write(
                self.style.SUCCESS('✅ Reviews created successfully!')
            )

            # Step 3: Create roles and users
            self.stdout.write(
                self.style.SUCCESS('👥 Step 3/3: Creating roles and users...')
            )
            call_command('create_roles')
            self.stdout.write(
                self.style.SUCCESS('✅ Roles and users created successfully!')
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
            self.stdout.write('   • Super User: super_user@mail.com | @dmin123')
            self.stdout.write('   • Inventory User: inventory_user@mail.com | @dmin123')
            self.stdout.write('   • Manager User: manager_user@mail.com | @dmin123')
            self.stdout.write('   • Reviewer User: reviewer_user@mail.com | @dmin123')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during setup: {str(e)}')
            )
            raise e

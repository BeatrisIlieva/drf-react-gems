# python manage.py generate_product_catalog
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from src.products.models.product import Earwear, Neckwear, Fingerwear, Wristwear
from src.products.models.inventory import Inventory
from src.products.models.review import Review
import os


class Command(BaseCommand):
    help = 'Generate comprehensive product catalog PDF from PostgreSQL database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='media/product_catalog.pdf',
            help='Output path for the PDF file (default: media/product_catalog.pdf)'
        )

    def handle(self, *args, **options):
        output_path = options['output']

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.stdout.write('Starting product catalog generation...')

        # Create PDF document with minimal styling
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build PDF content
        story = []
        styles = getSampleStyleSheet()

        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8
        )

        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 4

        # Add catalog header
        story.append(Paragraph("Complete Product Catalog", header_style))
        story.append(Spacer(1, 16))

        # Process each product type
        product_models = [
            ('Earring', Earwear),
            ('Necklace', Neckwear),
            ('Ring', Fingerwear),
            ('Bracelet', Wristwear)
        ]

        total_products = 0

        for category_name, model_class in product_models:
            # Get all products for this category
            products = model_class.objects.select_related(
                'collection', 'color', 'metal', 'stone'
            ).prefetch_related('inventory', 'review').all()

            if not products:
                continue

            # Process each product
            for product in products:
                total_products += 1

                # Get content type for this product
                content_type = ContentType.objects.get_for_model(model_class)

                inventory_items = Inventory.objects.filter(
                    content_type=content_type,
                    object_id=product.id
                ).select_related('size')

                sizes = ''

                for i, inventory in enumerate(inventory_items):
                    if i <= len(inventory_items) - 2:
                        sizes += f"Size: {inventory.size.name} - Price: ${inventory.price},"
                    else:
                        sizes += f"Size: {inventory.size.name} - Price: ${inventory.price}"

                average_rating = ''

                reviews = Review.objects.filter(
                    content_type=content_type,
                    object_id=product.id,
                    approved=True
                ).select_related('user')

                if reviews:
                    # Calculate average rating
                    total_rating = sum([review.rating for review in reviews])
                    avg_rating = total_rating / len(reviews)

                    average_rating = f'{avg_rating:.1f}/5 stars'

                # Basic product information - each property on new line
                basic_info = f"""
                Collection: {product.collection.name};
                Color: {product.color.name};
                Metal: {product.metal.name};
                Stone: {product.stone.name};
                Category: {'Watch' if category_name == 'Bracelet' and (product.collection.name == 'Bracelet' or product.collection.name == 'Classics') else category_name};
                Product ID: {product.id};
                Image URL: {product.first_image};
                Sizes: {sizes};
                Average Rating: {average_rating};
                """
                story.append(Paragraph(basic_info, normal_style))
                story.append(Spacer(1, 8))

                # Inventory information
                inventory_items = Inventory.objects.filter(
                    content_type=content_type,
                    object_id=product.id
                ).select_related('size')

        # Build the PDF
        doc.build(story)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created jewelry catalog PDF!\n'
                f'Location: {output_path}\n'
                f'Total products: {total_products}\n'
                f'You can find the file at: {os.path.abspath(output_path)}'
            )
        )

        return output_path

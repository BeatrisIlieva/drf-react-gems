# python manage.py generate_product_catalog


from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from src.products.models.inventory import Inventory
from src.products.models.product import Earwear, Neckwear, Fingerwear, Wristwear
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

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                leftMargin=0.5*inch, rightMargin=0.5*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)

        # Build PDF content
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )

        product_header_style = ParagraphStyle(
            'ProductHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=8
        )

        # Add title
        story.append(Paragraph("Complete Product Catalog", title_style))
        story.append(Spacer(1, 20))

        # Add generation timestamp
        from django.utils import timezone
        timestamp = timezone.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on: {timestamp}", styles['Normal']))
        story.append(Spacer(1, 30))

        # Process each product type
        product_models = [
            ('Earwear', Earwear),
            ('Neckwear', Neckwear),
            ('Fingerwear', Fingerwear),
            ('Wristwear', Wristwear)
        ]

        total_products = 0

        for category_name, model_class in product_models:
            # Add category header
            category_style = ParagraphStyle(
                'CategoryHeader',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=15,
                textColor=colors.darkred
            )
            story.append(
                Paragraph(f"{category_name} Products", category_style))
            story.append(Spacer(1, 10))

            # Get all products for this category
            products = model_class.objects.select_related(
                'collection', 'color', 'metal', 'stone'
            ).prefetch_related('inventory', 'review').all()

            if not products:
                story.append(
                    Paragraph("No products available in this category.", styles['Normal']))
                story.append(Spacer(1, 20))
                continue

            # Process each product
            for product in products:
                total_products += 1

                # Get content type for this product
                content_type = ContentType.objects.get_for_model(model_class)

                # Product header with unique identifier
                product_title = f"PRODUCT_ID_{content_type.id}_{product.id} - {product.collection.name} {category_name}"
                story.append(Paragraph(product_title, product_header_style))

                # Basic product information
                basic_info = f"""
                <b>Collection:</b> {product.collection.name}<br/>
                <b>Color:</b> {product.color.name}<br/>
                <b>Metal:</b> {product.metal.name}<br/>
                <b>Stone:</b> {product.stone.name}<br/>
                <b>Category:</b> {category_name}<br/>
                <b>Created:</b> {product.created_at.strftime('%B %d, %Y')}<br/>
                <b>Product Type ID:</b> {content_type.id}<br/>
                <b>Product ID:</b> {product.id}<br/>
                """
                story.append(Paragraph(basic_info, styles['Normal']))
                story.append(Spacer(1, 10))

                # Inventory information
                inventory_items = Inventory.objects.filter(
                    content_type=content_type,
                    object_id=product.id
                )

                if inventory_items:
                    story.append(
                        Paragraph("<b>Available Sizes & Pricing:</b>", styles['Heading3']))

                    # Create inventory table
                    inventory_data = [['Size', 'Price', 'Stock Quantity']]
                    for inventory in inventory_items:
                        inventory_data.append([
                            inventory.size.name,
                            f"${inventory.price}",
                            str(inventory.quantity)
                        ])

                    inventory_table = Table(inventory_data, colWidths=[
                                            1.5*inch, 1.5*inch, 1.5*inch])
                    inventory_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(inventory_table)
                    story.append(Spacer(1, 10))
                else:
                    story.append(
                        Paragraph("No inventory information available.", styles['Normal']))
                    story.append(Spacer(1, 5))

                # Reviews information
                reviews = Review.objects.filter(
                    content_type=content_type,
                    object_id=product.id,
                    approved=True  # Only show approved reviews
                )

                if reviews:
                    # Calculate average rating
                    total_rating = sum([review.rating for review in reviews])
                    avg_rating = total_rating / len(reviews)

                    review_info = f"""
                    <b>Customer Reviews:</b><br/>
                    Average Rating: {avg_rating:.1f}/5 stars ({len(reviews)} reviews)<br/>
                    """
                    story.append(Paragraph(review_info, styles['Normal']))

                    # Add individual review highlights (first 3 reviews)
                    for i, review in enumerate(reviews[:3]):
                        review_text = f"""
                        <b>★</b> {review.rating}/5 - {review.user.username}: 
                        "{review.comment}"
                        """
                        story.append(Paragraph(review_text, styles['Italic']))
                        if i < 2 and i < len(reviews) - 1:
                            story.append(Spacer(1, 5))

                    story.append(Spacer(1, 10))
                else:
                    story.append(
                        Paragraph("No customer reviews yet.", styles['Normal']))
                    story.append(Spacer(1, 5))

                # Image URLs (for reference)
                if product.first_image or product.second_image:
                    image_info = f"""
                    <b>Product Images:</b><br/>
                    Primary Image: {product.first_image}<br/>
                    Secondary Image: {product.second_image}<br/>
                    """
                    story.append(Paragraph(image_info, styles['Normal']))

                # Add separator between products
                story.append(Spacer(1, 15))
                story.append(Paragraph("─" * 80, styles['Normal']))
                story.append(Spacer(1, 15))

        # Add summary at the end
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            alignment=1,
            textColor=colors.darkblue
        )

        story.append(Paragraph("Catalog Summary", summary_style))
        summary_text = f"""
        Total Products in Catalog: {total_products}<br/>
        Categories: Earwear, Neckwear, Fingerwear, Wristwear<br/>
        Generated: {timestamp}
        """
        story.append(Paragraph(summary_text, styles['Normal']))

        # Build the PDF
        doc.build(story)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created product catalog PDF!\n'
                f'Location: {output_path}\n'
                f'Total products: {total_products}'
            )
        )

        # Display summary by category
        for category_name, model_class in product_models:
            count = model_class.objects.count()
            self.stdout.write(f'  {category_name}: {count} products')

        return output_path

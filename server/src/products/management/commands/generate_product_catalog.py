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

        # Minimal, clean styles for effective vectorization
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=12,
            alignment=1
        )

        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8
        )

        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 4

        # Add company header and information
        story.append(
            Paragraph("DRF React Gems - an online luxury jewelry store", title_style))
        story.append(Spacer(1, 12))

        company_description = """
        One of the most important aspects of the DRF React Gems design DNA is the ability to transform diamonds and precious gemstones into one-of-a-kind creations, through exceptional techniques in craftsmanship and design. Throughout its history, the House has had the opportunity to explore different artistic influences, which have helped to shape and define its fine jewelry aesthetic. In fact, DRF React Gems was known to hire classically trained artists to work as jewelry designers, because they had an innate understanding of the aspects that brought fine jewelry to life. Masterful design is transformative, as exceptional stones are vividly reimagined as jewels of distinction. Established in 1998, the House quickly gained recognition for its innovative approach to blending modern minimalism with timeless elegance, drawing inspiration from natural forms like ocean waves and celestial patterns to create pieces that evoke emotion and storytelling. Committed to ethical practices, DRF React Gems sources its gems from conflict-free mines and employs sustainable methods in its ateliers, ensuring each jewel not only captivates but also aligns with responsible luxury. Over the years, the House has expanded its collections to include customizable options, allowing clients to infuse personal narratives into heirloom-quality designs, while its limited-edition series often incorporate rare, colored diamonds that highlight the brand's expertise in color grading and cutting precision. This dedication to innovation and integrity has positioned DRF React Gems as a beacon of contemporary luxury, where every piece is a testament to enduring beauty and craftsmanship.
        """
        story.append(Paragraph(company_description, normal_style))
        story.append(Spacer(1, 16))

        # Product Care section
        story.append(Paragraph("Product Care", header_style))
        care_instructions = """
        Use a soft cloth to gently wipe clean, then remove any remaining impurities with mild diluted soap. Rinse with warm water and dry thoroughly before storing in the provided jewelry pouch. Do not use abrasive cleaners, steamers or ultrasonic machines.
        """
        story.append(Paragraph(care_instructions, normal_style))
        story.append(Spacer(1, 16))

        # Shipping section
        story.append(Paragraph("Complimentary one-day shipping", header_style))
        shipping_info = """
        Customer orders are completed within one day of being placed—no matter which day they order.
        """
        story.append(Paragraph(shipping_info, normal_style))
        story.append(Spacer(1, 24))

        story.append(Paragraph("Customer Reviews", header_style))
        customer_reviews = """
            Beautiful piece, exactly as described. The craftsmanship is impressive, and it really stands out on special occasions;
            The gemstone sparkles brilliantly in the light, catching everyone's attention. It adds just the right amount of sparkle to any outfit;
            A bit smaller than expected, but still lovely. It’s delicate and subtle, fitting perfectly with many styles;
            Shipping was fast and the packaging was excellent. The item arrived safely and looked brand new right out of the box;
            Perfect gift for a loved one, highly recommend! They wear it every day without fail;
            The attention to detail is remarkable. You can tell a lot of care went into making this piece. I’m very happy with my purchase;
            The stones are well set and the finish is flawless. It looks expensive but was surprisingly affordable;
            I bought this as a gift, and it was very well received. The recipient hasn’t taken it off since!,
            Comfortable, stylish, and well-made — everything I was looking for in a jewelry piece;
            This item exceeded my expectations for the price. It’s now a favorite in my collection;
            It looks great with both casual clothes and more formal attire, very versatile;
            I appreciate the durability — it’s been through daily wear and still looks new;
            The packaging was lovely, making it perfect for gifting right away;
            Subtle yet elegant — just the right touch without being too flashy. Works with all kinds of looks;
            Feels personal and thoughtfully made. It really shows that it’s crafted with intention;
            This piece has a timeless design that fits any style, whether minimal or bold;
            Matches beautifully with other accessories, and the quality is consistent across the board;
            It arrived ready to gift, with care in every detail — from the item itself to the packaging;
        """
        story.append(Paragraph(customer_reviews, normal_style))
        story.append(Spacer(1, 24))

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

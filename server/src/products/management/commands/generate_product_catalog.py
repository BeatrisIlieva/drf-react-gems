# python manage.py generate_product_catalog
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from src.products.models.product import Earwear, Neckwear, Fingerwear, Wristwear
from src.products.models.inventory import Inventory
from src.products.models.review import Review
import os
import requests
from io import BytesIO
from PIL import Image as PILImage


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
        
        product_title_style = ParagraphStyle(
            'ProductTitle',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 4
        
        # Add company header and information
        story.append(Paragraph("DRF React Gems - an online luxury jewelry store", title_style))
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
        
        # Add catalog header
        story.append(Paragraph("Complete Product Catalog", header_style))
        story.append(Spacer(1, 16))
        
        # Process each product type
        product_models = [
            ('Earwear', Earwear),
            ('Neckwear', Neckwear), 
            ('Fingerwear', Fingerwear),
            ('Wristwear', Wristwear)
        ]
        
        total_products = 0
        
        for category_name, model_class in product_models:
            # Get all products for this category
            products = model_class.objects.select_related(
                'collection', 'color', 'metal', 'stone'
            ).prefetch_related('inventory', 'review').all()
            
            if not products:
                continue
            
            # Add category header
            story.append(Paragraph(f"{category_name} Collection", header_style))
            story.append(Spacer(1, 8))
            
            # Process each product
            for product in products:
                total_products += 1
                
                # Get content type for this product
                content_type = ContentType.objects.get_for_model(model_class)
                
                # Product identifier for chatbot reference
                product_title = f"PRODUCT_ID_{content_type.id}_{product.id} {product.collection.name} {category_name}"
                story.append(Paragraph(product_title, product_title_style))
                
                # Add product images
                story.extend(self._add_product_images(product, styles))
                
                # Basic product information - each property on new line
                basic_info = f"""
                Collection: {product.collection.name}<br/>
                Color: {product.color.name}<br/>
                Metal: {product.metal.name}<br/>
                Stone: {product.stone.name}<br/>
                Category: {category_name}<br/>
                Content Type ID: {content_type.id}<br/>
                Product ID: {product.id}<br/>
                Created: {product.created_at.strftime('%B %d, %Y')}
                """
                story.append(Paragraph(basic_info, normal_style))
                story.append(Spacer(1, 8))
                
                # Inventory information
                inventory_items = Inventory.objects.filter(
                    content_type=content_type,
                    object_id=product.id
                ).select_related('size')
                
                if inventory_items:
                    story.append(Paragraph("Available Sizes and Pricing:", product_title_style))
                    
                    for inventory in inventory_items:
                        size_info = f"Size: {inventory.size.name}<br/>Price: ${inventory.price}<br/>Available Stock: {inventory.quantity} pieces"
                        story.append(Paragraph(size_info, normal_style))
                        story.append(Spacer(1, 4))
                    
                    story.append(Spacer(1, 8))
                
                # Complete reviews information (no slicing)
                reviews = Review.objects.filter(
                    content_type=content_type,
                    object_id=product.id,
                    approved=True
                ).select_related('user')
                
                if reviews:
                    # Calculate average rating
                    total_rating = sum([review.rating for review in reviews])
                    avg_rating = total_rating / len(reviews)
                    
                    review_header = f"Customer Reviews: {avg_rating:.1f}/5 stars ({len(reviews)} reviews)"
                    story.append(Paragraph(review_header, product_title_style))
                    
                    # Add all complete reviews - simplified format
                    for review in reviews:
                        review_text = f"Rating: {review.rating}/5 stars<br/>Customer Review: {review.comment}"
                        story.append(Paragraph(review_text, normal_style))
                        story.append(Spacer(1, 6))
                else:
                    story.append(Paragraph("No customer reviews available.", normal_style))
                
                # Simple spacing between products
                story.append(Spacer(1, 20))
        
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
    
    def _add_product_images(self, product, styles):
        """Add product images to the PDF with better error handling"""
        story_elements = []
        
        for i, image_url in enumerate([product.first_image, product.second_image]):
            if image_url:
                try:
                    print(f"Processing image {i+1}: {image_url[:50]}...")  # Debug output
                    
                    # Download image with shorter timeout and headers
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(image_url, timeout=5, headers=headers)
                    
                    if response.status_code == 200:
                        # Convert to PIL Image for processing
                        img_data = BytesIO(response.content)
                        pil_img = PILImage.open(img_data)
                        
                        # Convert to RGB and remove any background
                        if pil_img.mode in ('RGBA', 'LA', 'P'):
                            # Create white background for transparent images
                            background = PILImage.new('RGB', pil_img.size, (255, 255, 255))
                            if pil_img.mode == 'RGBA':
                                background.paste(pil_img, mask=pil_img.split()[-1])
                            else:
                                background.paste(pil_img)
                            pil_img = background
                        
                        # Resize for PDF (max width 1.5 inches for better performance)
                        max_width = 1.5 * inch
                        aspect_ratio = pil_img.width / pil_img.height
                        
                        if pil_img.width > max_width:
                            new_width = max_width
                            new_height = max_width / aspect_ratio
                        else:
                            new_width = pil_img.width * 0.75  # Scale down even small images
                            new_height = pil_img.height * 0.75
                        
                        # Save processed image to BytesIO
                        processed_img = BytesIO()
                        pil_img.save(processed_img, format='JPEG', quality=85)
                        processed_img.seek(0)
                        
                        # Create reportlab Image
                        img = Image(processed_img, width=new_width, height=new_height)
                        story_elements.append(img)
                        story_elements.append(Spacer(1, 6))
                        
                        # Add image URL for reference (for chatbot)
                        story_elements.append(Paragraph(f"Image URL: {image_url}", styles['Normal']))
                        story_elements.append(Spacer(1, 4))
                        
                        print(f"✓ Successfully processed image {i+1}")
                        
                except requests.exceptions.Timeout:
                    print(f"✗ Image {i+1} timed out: {image_url}")
                    story_elements.append(Paragraph(f"Image URL: {image_url} (Timeout)", styles['Normal']))
                    story_elements.append(Spacer(1, 4))
                    
                except requests.exceptions.RequestException as e:
                    print(f"✗ Image {i+1} request failed: {str(e)}")
                    story_elements.append(Paragraph(f"Image URL: {image_url} (Network error)", styles['Normal']))
                    story_elements.append(Spacer(1, 4))
                    
                except Exception as e:
                    print(f"✗ Image {i+1} processing failed: {str(e)}")
                    story_elements.append(Paragraph(f"Image URL: {image_url} (Processing error)", styles['Normal']))
                    story_elements.append(Spacer(1, 4))
        
        return story_elements
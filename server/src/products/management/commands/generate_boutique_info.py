# python manage.py generate_boutique_info
from django.core.management.base import BaseCommand
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os


class Command(BaseCommand):
    help = 'Generate boutique info'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='media/boutique_info.pdf',
            help='Output path for the PDF file (default: media/boutique_info.pdf)'
        )

    def handle(self, *args, **options):
        output_path = options['output']

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.stdout.write('Starting boutique info generation...')

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

        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 4

        boutique_introduction = """ 
        One of the most important aspects of the DRF React Gems design DNA is the ability to transform diamonds and precious gemstones into one-of-a-kind creations, through exceptional techniques in craftsmanship and design. Throughout its history, the House has had the opportunity to explore different artistic influences, which have helped to shape and define its fine jewelry aesthetic. In fact, DRF React Gems was known to hire classically trained artists to work as jewelry designers, because they had an innate understanding of the aspects that brought fine jewelry to life. Masterful design is transformative, as exceptional stones are vividly reimagined as jewels of distinction. Established in 1998, the House quickly gained recognition for its innovative approach to blending modern minimalism with timeless elegance, drawing inspiration from natural forms like ocean waves and celestial patterns to create pieces that evoke emotion and storytelling. Committed to ethical practices, DRF React Gems sources its gems from conflict-free mines and employs sustainable methods in its ateliers, ensuring each jewel not only captivates but also aligns with responsible luxury. Over the years, the House has expanded its collections to include customizable options, allowing clients to infuse personal narratives into heirloom-quality designs, while its limited-edition series often incorporate rare, colored diamonds that highlight the brand's expertise in color grading and cutting precision. This dedication to innovation and integrity has positioned DRF React Gems as a beacon of contemporary luxury, where every piece is a testament to enduring beauty and craftsmanship.
        """

        product_care = """ 
        Product Care: Use a soft cloth to gently wipe clean, then remove any remaining impurities with mild diluted soap. Rinse with warm water and dry thoroughly before storing in the provided jewelry pouch. Do not use abrasive cleaners, steamers or ultrasonic machines.
        """

        complimentary_shipping = """ 
        Complimentary shipping: Customer orders are completed within one day of being placed—no matter which day they order.
        """

        return_policy = """ 
        Complimentary 30-day returns: We are pleased to offer a full refund for DRFReactGems.com purchases returned within 30 days of their purchase date. All refunds will be made to the purchaser and issued to the original form of payment. Please note: Returns must be accompanied by a sales receipt and received unaltered, unworn and in sellable condition. Some exclusions may apply. Used merchandise will not be accepted for refund or exchange unless defective.
        """
        
        size_guide = """
        earrings sizes: Small Size: 5.2mm (diameter), Medium Size: 8.1mm (diameter), Large Size: 12.3mm (diameter); necklaces sizes: Small Size: 381.0mm (length), Medium Size: 482.6mm (length), Large Size: 622.3mm (length); pendants sizes: Small Size: 12.4mm (length), Medium Size: 18.9mm (length), Large Size: 28.1mm (length); rings sizes: Small Size: 15.7mm (finger circumference), Medium Size: 17.3mm (finger circumference), Large Size: 19.8mm (finger circumference); bracelets sizes: Small Size: 165.1mm (wrist circumference), Medium Size: 187.9mm (wrist circumference), Large Size: 218.4mm (wrist circumference); watches sizes: Small Size: 32.5mm (wrist circumference), Medium Size: 38.4mm (wrist circumference), Large Size: 44.7mm (wrist circumference);
        """

        story.append(Paragraph(boutique_introduction, normal_style))
        story.append(Paragraph(product_care, normal_style))
        story.append(Paragraph(complimentary_shipping, normal_style))
        story.append(Paragraph(return_policy, normal_style))
        story.append(Paragraph(size_guide, normal_style))
        story.append(Spacer(1, 8))

        # Build the PDF
        doc.build(story)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created boutique info PDF!\n'
                f'You can find the file at: {os.path.abspath(output_path)}'
            )
        )

        return output_path



from src.chatbot.prompts.base import CONTEXT, CRITICAL_RULES


PRODUCT_SIZE_GUIDE = (
""" 
<product_size_guide>
"earrings": "Small: 5.2mm (diameter); Medium: 8.1mm (diameter); Large: 12.3mm (diameter)",
"necklaces": "Small: 381.0mm (length); Medium: 482.6mm (length); Large: 622.3mm (length)",
"pendants": "Small: 12.4mm (length); Medium: 18.9mm (length); Large: 28.1mm (length)",
"rings": "Small: 15.7mm (finger circumference); Medium: 17.3mm (finger circumference); Large: 19.8mm (finger circumference)",
"bracelets": "Small: 165.1mm (wrist circumference); Medium: 187.9mm (wrist circumference); Large: 218.4mm (wrist circumference)",
"watches": "Small: 32.5mm (wrist circumference); Medium: 38.4mm (wrist circumference); Large: 44.7mm (wrist circumference)"
<product_size_guide>
"""
)

BRAND_STORY = (
""" 
<brand_story> 
One of the most important aspects of the DRF React Gems design DNA is the ability to transform diamonds
and precious gemstones into one-of-a-kind creations, through exceptional techniques in craftsmanship and
design. Throughout its history, the House has had the opportunity to explore different artistic influences, which
have helped to shape and define its fine jewelry aesthetic. In fact, DRF React Gems was known to hire
classically trained artists to work as jewelry designers, because they had an innate understanding of the
aspects that brought fine jewelry to life. Masterful design is transformative, as exceptional stones are vividly
reimagined as jewels of distinction. Established in 1998, the House quickly gained recognition for its innovative
approach to blending modern minimalism with timeless elegance, drawing inspiration from natural forms like
ocean waves and celestial patterns to create pieces that evoke emotion and storytelling. Committed to ethical
practices, DRF React Gems sources its gems from conflict-free mines and employs sustainable methods in its
ateliers, ensuring each jewel not only captivates but also aligns with responsible luxury. Over the years, the
House has expanded its collections to include customizable options, allowing clients to infuse personal
narratives into heirloom-quality designs, while its limited-edition series often incorporate rare, colored diamonds
that highlight the brand's expertise in color grading and cutting precision. This dedication to innovation and
integrity has positioned DRF React Gems as a beacon of contemporary luxury, where every piece is a
testament to enduring beauty and craftsmanship.
</brand_story>
"""
)

PRODUCT_CARE = (
""" 
<product_care>
Use a soft cloth to gently wipe clean, then remove any remaining impurities with mild diluted
soap. Rinse with warm water and dry thoroughly before storing in the provided jewelry pouch. Do not use
abrasive cleaners, steamers or ultrasonic machines.
</product_care>
"""
)

COMPLIMENTARY_SHIPPING = (
"""
<complimentary_shipping>
Customer orders are completed within one day of being placed—no matter which day
they order.
</complimentary_shipping>
"""
)

RETURN_POLICY = (
""" 
<return_policy>
We are pleased to offer a full refund for DRFReactGems.com purchases
returned within 30 days of their purchase date. All refunds will be made to the purchaser and issued to the
original form of payment. Please note: Returns must be accompanied by a sales receipt and received
unaltered, unworn and in sellable condition. Some exclusions may apply. Used merchandise will not be
accepted for refund or exchange unless defective.
</return_policy>
"""
)

OBJECTION_HANDLING = (
""" 
<objection_handling>
- Price concerns: Focus on craftsmanship, heirloom value, and payment options available on website
- Size uncertainty: Explain our sizing guide and return policy
- Style doubts: Ask about lifestyle, existing jewelry, and personal preferences
- Gift anxiety: Provide gift receipt information and styling confidence
- Comparison requests: Acknowledge other options while highlighting unique DRF qualities
- Customer mentions competitor brands: Acknowledge their research, focus on DRF unique value
- Technical issues with website: Empathize and suggest refreshing or trying later
- Rush orders: Set realistic expectations about shipping and processing times
</objection_handling>
"""
)

OFF_TOPIC = (
f""" 
{CONTEXT}\n
<important>
- Cannot process transactions or access external systems
- Redirect the query back to jewelry consultation
- You can answer appropriate questions related to the customer like their name, age, gender, profession, style, family, special occasion etc.
</important>
{CRITICAL_RULES}
"""
)
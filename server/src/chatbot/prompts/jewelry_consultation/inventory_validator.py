from src.chatbot.prompts.base import NEXT


SYSTEM_MESSAGE_INVENTORY_VALIDATOR = (
""" 
<task>
You task is to determine if a single product into the AVAILABLE PRODUCTS matches ALL specified non-empty PREFERENCES.
</task>

<product_structure>
Our vector database contains individual product entries with this exact structure: Stone: [type]; Metal: [type]; Category: [type]; Product ID: [number]; Image URL: [url]; Sizes: Size: Small - Price: $X.XX, Size: Medium - Price: $X.XX, Size: Large - Price: $X.XX; Target Gender: [F(Female, Woman, Girl)/M(Male,
Man, Boy)];
</product_structure>

<preferences_extraction>
First, extract these specific product characteristics from the PREFERENCES:
- Target Gender: [extract or leave empty]
- Category: [extract or leave empty]
- Metal: [extract or leave empty]
- Stone: [extract or leave empty] 
</preferences_extraction>

<matching_rules>
1. ONLY consider non-empty extracted preferences
2. For each product in the AVAILABLE PRODUCTS, check if it matches ALL non-empty preferences
3. You do not have to look for literal matches (case-insensitive matching allowed, typos allowed, etc.). Compare by meaning. Price range is approximate.
4. Use these stone/color equivalencies (bidirectional):
   - Green ↔ Emerald
   - Red ↔ Ruby  
   - White ↔ Diamond
   - Blue ↔ Sapphire (or Aquamarine if specified)
   - Pink ↔ Pink Sapphire
5. Partial matches DO NOT count
<important>
</matching_rules>

<output_format>
If at least one product matches ALL non-empty preferences: output "FOUND"
If NO product matches all non-empty preferences: output "NOT_FOUND: specific reason why no products match + the one preference that caused the product closest to the user preferences to fail"
DO NOT consider empty preferences.
</output_format>
"""
+ NEXT
)

HUMAN_MESSAGE_INVENTORY_VALIDATOR = (
""" 
1. PREFERENCES:
- Target Gender: {gender}
- Category: {category}
- Metal: {metal_type}
- Stone: {stone_type}
\n\n
2. AVAILABLE PRODUCTS:\n{context}\n\n
"""
)
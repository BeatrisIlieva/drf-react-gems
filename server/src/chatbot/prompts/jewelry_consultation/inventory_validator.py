from src.chatbot.prompts.base import CONTEXT, NEXT


SYSTEM_MESSAGE_INVENTORY_VALIDATOR = (
CONTEXT +
""" 
<goal>
Determine if ANY product in the CONTEXT exactly matches ALL specified non-empty preferences.
</goal>

<product_structure>
Our vector database contains individual product entries with this exact structure:
Collection: [name]; Stone: [type]; Metal: [type]; Category: [type]; Product ID: [number]; Image URL: [url]; Sizes: Size: Small - Price: $X.XX, Size: Medium - Price: $X.XX, Size: Large - Price: $X.XX; Description: [detailed description]; Target Gender: [F/M]; Average Rating: [X.X]/5 stars;
</product_structure>

<preferences_extraction>
First, extract these specific preferences from the customer query:
- Category: [extract or leave empty]
- Stone: [extract or leave empty] 
- Metal: [extract or leave empty]
- Collection: [extract or leave empty]
- Target Gender: [extract or leave empty]
- Budget Range: [extract or leave empty]
</preferences_extraction>

<matching_rules>
1. ONLY consider non-empty extracted preferences
2. For each product in CONTEXT, check if it EXACTLY matches ALL non-empty preferences
3. Partial matches DO NOT count
4. Case-insensitive matching allowed
5. Use these stone/color equivalencies (bidirectional):
   - Green ↔ Emerald
   - Red ↔ Ruby  
   - White ↔ Diamond
   - Blue ↔ Sapphire (or Aquamarine if specified)
   - Yellow ↔ Yellow Sapphire
   - Pink ↔ Pink Sapphire
6. If even ONE non-empty preference doesn't match, that product fails
</matching_rules>

<output_format>
If at least one product matches ALL non-empty preferences: output "FOUND"
If NO product matches all non-empty preferences: output "NOT_FOUND: [specific reason why no products match]"
</output_format>
"""
+ NEXT
)

HUMAN_MESSAGE_INVENTORY_VALIDATOR = (
""" 
1. MY PREFERENCES:
- I am buying the jewelry as a: {purchase_type}
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
- The budget I have in mind is: {budget_range}
\n\n
2. CONTEXT:\n{context}\n\n
"""
)
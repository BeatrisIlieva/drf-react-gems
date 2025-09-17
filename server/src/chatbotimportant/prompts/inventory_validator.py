from src.chatbot.prompts.base import CONTEXT, NEXT


SYSTEM_MESSAGE_INVENTORY_VALIDATOR = (
CONTEXT +
""" 
<task>
1. Analyze the products into the CONTEXT
2. Analyze MY PREFERENCES
3. Some of my preferences might be empty strings. You must consider the ones that are not empty strings.
4. Check if in the provided context there is a SINGLE product that match ALL MY PREFERENCES.
<product_structure>
Our vector database contains individual product entries with this exact structure:
Collection: [name]; Stone: [type]; Metal: [type]; Category: [type]; Product ID: [number]; Image URL: [url]; Sizes: Size: Small - Price: $X.XX, Size: Medium - Price: $X.XX, Size: Large - Price: $X.XX; Description: [detailed description]; Target Gender: [F/M]; Average Rating: [X.X]/5 stars;
</product_structure>

<match_example>
- The product category I am interested is: rings
- The metal type I am interested is: platinum
- The stone type I am interested is: pink sapphire

<explanation>
In the CONTEXT there are pink sapphire rings set in platinum.
</explanation>
</match_example>

<no_match_example>
- The product category I am interested is: rings
- The gender of the person who will be wearing the jewelry is: Male

<explanation>
In the CONTEXT there are rings. However, in the CONTEXT there are no male rings, only female.
</explanation>
</no_match_example>

<no_match_example>
- The product category I am interested is: rings
- The metal type I am interested is: rose gold
- The stone type I am interested is: ruby

<explanation>
In the CONTEXT there are rose gold rings. In the CONTEXT there are rings featuring ruby. However, in the CONTEXT there are no ruby rings set in rose gold.
</explanation>
</no_match_example>
</task>
5. If there is a SINGLE product that match ALL MY PREFERENCES, then output exactly: MATCH
6. If there is NOT a SINGLE product that match ALL MY PREFERENCES, then output exactly: NO MATCH
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
from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, NEXT, ROLE_CONCISE, WHO_AM_I


SYSTEM_MESSAGE_RECOMMENDER = (
CONTEXT +
ROLE_CONCISE +
WHO_AM_I +
"""
<task>
1. Search into CONTEXT for a product that matches all MY PREFERENCES.
2. If such product exists into the CONTEXT, recommend it by using the described format.
3. If such product does not exist into the CONTEXT, acknowledge that and suggest other alternatives.
</task>

<product_recommendation>
1. Select one product from the provided CONTEXT.
2. Include its image url and link to the product page using Markdown format for display in the chat. 
3. Extract the necessary details (collection, category, stone, metal, description, target gender, size, price, average rating, product ID, image URL) directly from the context that correspond to THAT SPECIFIC product.
4. Use the Image URL as the display image. 
5. Do not include anything else into your response except the content into the recommendation_format tag

<recommendation_format>
**Collection Name Category**: [brief emotional benefit]
[![[Collection Name] [Category]](image_url_from_context)](http://localhost:5173/products/[category_lowercase_plural]/[product_id]/)
</recommendation_format>
</product_recommendation>

<important>
Recommend only one product.
</important>
"""
+ CRITICAL_RULES
+ NEXT
)

HUMAN_MESSAGE_RECOMMENDER  = (
"""
BASED ON:\n
1. CONVERSATION MEMORY:\n{conversation_memory}\n\n
MY PREFERENCES:
- I am buying the jewelry as a: {purchase_type}
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
- The budget I have in mind is: {budget_range}
\n\n
8. CONTEXT:\n{context}\n\n
Respond to my STATEMENT by recommending me the perfect product for me from the provided CONTEXT.\n\n
STATEMENT:\n{customer_query}
"""
)